from typing import Protocol
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_response import GetBusyCouriersResponse
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_query import GetBusyCouriersQuery


class IGetIncompletedOrdersHandler(Protocol):
    async def handle(self, query: GetBusyCouriersQuery) -> GetBusyCouriersResponse:
        ...