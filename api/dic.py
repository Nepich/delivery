from typing import Iterator
from that_depends import BaseContainer, ContextScopes, providers

from api.mediator import Mediator
from core.application.domain_event_handlers.order_finished_handler import OrderFinishedHandler
from core.application.use_cases.commands.assigne.assigne_command import AssigneCommand
from core.application.use_cases.commands.assigne.assigne_handler import AssigneHandler
from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand
from core.application.use_cases.commands.create_order.create_order_handler import CreateOrderHandler
from core.application.use_cases.commands.move_couriers.move_couriers_command import MoveCourierCommand
from core.application.use_cases.commands.move_couriers.move_couriers_handler import MoveCourierHandler
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_handler import GetBusyCouriersHandler
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_query import GetBusyCouriersQuery
from core.application.use_cases.queries.get_incompleted_orders.get_incompleted_orders_handler import GetIncompletedOrdersHandler
from core.application.use_cases.queries.get_incompleted_orders.get_incompleted_orders_query import GetIncompletedOrdersQuery
from core.domain.order_aggregate.domain_events.order_finished_event import OrderFinishedEvent
from core.domain.services.dispatch_service import DispatchService
from core.primitives.imediator import IMediator
from infrastructure.adapters.grpc.geo_grpc import GeoGrpc
from infrastructure.adapters.kafka.producer import KafkaBus
from infrastructure.adapters.postgres.courier_repository import CourierRepository
from infrastructure.adapters.postgres.order_repository import OrderRepository
from infrastructure.adapters.postgres.uow import UnitOfWork
from infrastructure.settings import mq_settings


def configure_create_mediator(
    mediator: IMediator, 
    move_courier_handler, 
    create_order_handler,
    get_busy_courier_handler,
    get_incompleted_orders_handler,
    order_finished_handler
    ) -> Iterator[IMediator]:
    try:
        mediator.register(MoveCourierCommand, move_courier_handler)
        mediator.register(AssigneCommand, create_order_handler)
        mediator.register(CreateOrderCommand, move_courier_handler)
        mediator.register(GetBusyCouriersQuery, get_busy_courier_handler)
        mediator.register(GetIncompletedOrdersQuery, get_incompleted_orders_handler)
        mediator.register(OrderFinishedEvent, order_finished_handler)
        yield mediator
    finally:
        ...
        
        
class DIContainer(BaseContainer):
    premediator = providers.Factory(
        Mediator
    )
    dispatch_service = providers.Factory(DispatchService)
    courier_repository = providers.Factory(CourierRepository)
    order_repository = providers.Factory(OrderRepository)
    geo_grpc = providers.Factory(
        GeoGrpc,
        target="localhost:5004"
    )
    create_order_handler = providers.Factory(
        CreateOrderHandler, 
        repo=order_repository,
        geo_client=geo_grpc
        )
    get_busy_courier_handler = providers.Factory(
        GetBusyCouriersHandler
        )
    get_incompleted_orders_handler = providers.Factory(
        GetIncompletedOrdersHandler
        )
    message_bus = providers.Factory(
        KafkaBus,
        servers=mq_settings.DESTINATION,
        mediator=premediator,
        event_topics=""
    )
    order_finished_handler = providers.Factory(
        OrderFinishedHandler,
        message_bus=message_bus
        )
    uow = providers.Factory(
        UnitOfWork,
        courier_repo=courier_repository,
        order_repo=order_repository,
        mediator=premediator
        )
    move_courier_handler = providers.Factory(
        MoveCourierHandler,
        uow=uow,
        order_repo=order_repository,
        courier_repo=courier_repository
        )
    assign_handler = providers.Factory(
        AssigneHandler,
        uow=uow,
        courier_repo=courier_repository,
        order_repo=order_repository,
        dispatch_service=dispatch_service
        )
    mediator = providers.Resource(
        configure_create_mediator,
        premediator.cast,
        move_courier_handler.cast,
        create_order_handler.cast,
        get_busy_courier_handler.cast,
        get_incompleted_orders_handler.cast,
        order_finished_handler.cast,
        )