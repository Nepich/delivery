from dataclasses import dataclass
from core.application.use_cases.commands.move_couriers.move_couriers_command import MoveCourierCommand
from core.ports.icourier_repository import ICourierRepository
from core.ports.iorder_repository import IOrderRepository
from infrastructure.adapters.postgres.uow import UnitOfWork


@dataclass(frozen=True, slots=True)
class MoveCourierHandler:
    order_repo: IOrderRepository
    courier_repo: ICourierRepository
    uow: UnitOfWork
    
    async def handle(self, command: MoveCourierCommand):
        assigned_orders = await self.order_repo.get_assigned_orders()
        for order in assigned_orders:
            courier = await self.courier_repo.get_courier(courier_id=order.courier_id)
            courier.move(destination=order.location)
            
            if order.location == courier.location:
                order.complete()
                courier.set_free()
                async with self.uow() as session:
                    await self.order_repo.update_order(session=session, order=order)
                    await self.courier_repo.update_courier(session=session, courier=courier)
                continue
            
            async with self.uow() as session:
                await self.courier_repo.update_courier(session=session, courier=courier)