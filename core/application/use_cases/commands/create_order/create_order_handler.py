from dataclasses import dataclass
from random import randint

from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand
from core.domain.order_aggregate.order import Order
from core.domain.shared_kernel.location import Location
from core.ports.iorder_repository import IOrderRepository


@dataclass(slots=True, frozen=True)
class CreateOrderHandler:
    repo: IOrderRepository
    
    async def handle(self, command: CreateOrderCommand):
        order = Order(
            id=command.basket_id,
            location=Location( #TODO change to intagration
                    x=randint(1,10),
                    y=randint(1,10),
                )
            )
        await self.repo.add_order(order=order)
        
        return True
    
    def __hash__(self):
        return hash(self.__class__.__name__)