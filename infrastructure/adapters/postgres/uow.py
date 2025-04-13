from dataclasses import dataclass
from api.mediator import Mediator
from core.domain.courier_aggregate.courier import Courier
from core.domain.order_aggregate.order import Order
from infrastructure.adapters.postgres.session import async_session
from infrastructure.adapters.postgres.courier_repository import CourierRepository
from infrastructure.adapters.postgres.order_repository import OrderRepository


@dataclass(slots=True, frozen=True)
class UnitOfWork:
    courier_repo: CourierRepository
    order_repo: OrderRepository
    mediator: Mediator
    
    async def assigne_courier_to_order(self, courier: Courier, order: Order):
        async with async_session() as session, session.begin():
            await self.order_repo.update_order(order=order)
            await self.courier_repo.update_courier(courier=courier)
            await session.commit()
            
    async def move_courier(self, courier: Courier, order: Order):
        async with async_session() as session, session.begin():
            await self.order_repo.update_order(order=order)
            await self.courier_repo.update_courier(courier=courier)
            await session.commit()
            await self.mediator.publish(order.get_domain_events.pop())
            order.clear_domain_events()