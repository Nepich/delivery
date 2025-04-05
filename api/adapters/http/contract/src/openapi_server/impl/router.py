from typing import List
from uuid import uuid4
from that_depends import Provide, inject
from api.adapters.http.contract.src.openapi_server.apis.default_api_base import BaseDefaultApi
from api.adapters.http.contract.src.openapi_server.models.courier import Courier
from api.adapters.http.contract.src.openapi_server.models.order import Order
from api.dic import DIContainer
from api.mediator import Mediator
from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_query import GetBusyCouriersQuery
from core.application.use_cases.queries.get_incompleted_orders.get_incompleted_orders_query import GetIncompletedOrdersQuery


class Router(BaseDefaultApi):
    
    def __init__(self, mediator: Mediator = Provide[DIContainer.mediator.sync_resolve()]):
        self.mediator = mediator
        
    async def create_order(
        self,
    ) -> None:
        """Позволяет создать заказ с целью тестирования"""
        fake_data = {
            "basket_id": uuid4(),
            "street_name": "some_ name"
            }
        command = CreateOrderCommand(**fake_data).model_validate()
        return await self.mediator.notify(command=command)


    async def get_couriers(
        self,
    ) -> List[Courier]:
        """Позволяет получить всех курьеров"""
        command = GetBusyCouriersQuery()
        return await self.mediator.notify(command=command)


    async def get_orders(
        self,
    ) -> List[Order]:
        """Позволяет получить все незавершенные"""
        command = GetIncompletedOrdersQuery()
        return await self.mediator.notify(command=command)