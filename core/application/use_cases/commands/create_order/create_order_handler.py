from dataclasses import dataclass

from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand
from core.domain.order_aggregate.order import Order
from core.ports.igeo_grpc import IGeoGrpc
from core.ports.iorder_repository import IOrderRepository
from infrastructure.adapters.grpc.out.geo_pb2 import GetGeolocationRequest


@dataclass(slots=True, frozen=True)
class CreateOrderHandler:
    repo: IOrderRepository
    geo_grpc: IGeoGrpc
    
    async def handle(self, command: CreateOrderCommand):
        location = self.geo_grpc.GetGeolocation(
            request=GetGeolocationRequest(Street="some_street")
            )
        order = Order(
            id=command.basket_id,
            location=location
            )
        await self.repo.add_order(order=order)
        
        return True
    
    def __hash__(self):
        return hash(self.__class__.__name__)