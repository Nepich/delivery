
from that_depends import BaseContainer, providers

from api.mediator import Mediator
from core.application.use_cases.commands.assigne.assigne_handler import AssigneHandler
from core.application.use_cases.commands.create_order.create_order_handler import CreateOrderHandler
from core.application.use_cases.commands.move_couriers.move_couriers_handler import MoveCourierHandler
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_handler import GetBusyCouriersHandler
from core.application.use_cases.queries.get_incompleted_orders.get_incompleted_orders_handler import GetIncompletedOrdersHandler
from core.domain.services.dispatch_service import DispatchService
from infrastructure.adapters.postgres.courier_repository import CourierRepository
from infrastructure.adapters.postgres.order_repository import OrderRepository
from infrastructure.adapters.postgres.uow import UnitOfWork


class DIContainer(BaseContainer):
    dispatch_service = providers.Factory(DispatchService)
    courier_repository = providers.Factory(CourierRepository)
    order_repository = providers.Factory(OrderRepository)
    uow = providers.Factory(
        UnitOfWork,
        courier_repo=courier_repository,
        order_repo=order_repository
        )
    assign_handler = providers.Factory(
        AssigneHandler,
        uow=uow,
        courier_repo=courier_repository,
        order_repo=order_repository,
        dispatch_service=dispatch_service
        )
    create_order_handler = providers.Factory(
        CreateOrderHandler, repo=order_repository
        )
    move_courier_handler = providers.Factory(
        MoveCourierHandler,
        order_repo=order_repository,
        courier_repo=courier_repository
        )
    get_busy_courier_handler = providers.Factory(
        GetBusyCouriersHandler
        )
    get_incompleted_orders_handler = providers.Factory(
        GetIncompletedOrdersHandler
        )
    mediator = providers.Factory(
        Mediator,
        assign_handler=assign_handler,
        create_order_handler=create_order_handler,
        move_courier_handler=move_courier_handler,
        get_busy_courier_handler=get_busy_courier_handler,
        get_incompleted_orders_handler=get_incompleted_orders_handler
    )