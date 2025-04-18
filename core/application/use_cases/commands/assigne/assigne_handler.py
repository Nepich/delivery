from dataclasses import dataclass

from core.application.use_cases.commands.assigne.assigne_command import AssigneCommand
from core.domain.services.idispatch_service import IDispatchService
from core.ports.icourier_repository import ICourierRepository
from core.ports.iorder_repository import IOrderRepository
from infrastructure.adapters.postgres.uow import UnitOfWork


@dataclass(frozen=True, slots=True)
class AssigneHandler:
    uow: UnitOfWork
    courier_repo: ICourierRepository
    order_repo: IOrderRepository
    dispatch_service: IDispatchService
        
    async def handle(self, command: AssigneCommand):
        order = await self.order_repo.get_new_order()
        couriers = await self.courier_repo.get_free_couriers()
        
        try:
            best_courier = self.dispatch_service.dispatch(
                order=order, couriers=couriers
                )
        except Exception:
            return False
        
        async with self.uow() as session:
            await self.order_repo.update_order(session=session, order=order)
            await self.courier_repo.update_courier(session=session, courier=best_courier)

        return True
        