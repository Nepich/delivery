from typing import Protocol, TYPE_CHECKING

from core.domain.courier_aggregate.courier import Courier
from core.domain.order_aggregate.order import Order


class IDispatchService(Protocol):
    
    def dispatch(self, order: Order, couriers: list[Courier]) -> Courier:
        ...