from typing import Iterator
from apscheduler.triggers.interval import IntervalTrigger
from that_depends import BaseContainer, providers
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from api.mediator import Mediator
from api.scheduler import Scheduler
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
from core.domain.order_aggregate.domain_events.order_finished_event import OrderFinished
from core.domain.services.dispatch_service import DispatchService
from core.primitives.imediator import IMediator
from infrastructure.adapters.grpc.geo_grpc import GeoGrpc
from infrastructure.adapters.kafka.producer import KafkaBus
from infrastructure.adapters.postgres.courier_repository import CourierRepository
from infrastructure.adapters.postgres.entities.event import Event
from infrastructure.adapters.postgres.jobs.outbox_job import OutboxJob
from infrastructure.adapters.postgres.order_repository import OrderRepository
from infrastructure.adapters.postgres.uow import UnitOfWork
from infrastructure.settings import DBSettings, mq_settings


def configure_created_message_bus(
    bus: KafkaBus
    ) -> Iterator[KafkaBus]:
    try:
        bus.register_topic(OrderFinished, "order.status.changed")
        yield bus
    finally:
        ...
        
        
def configure_scheduler(
    scheduler: Scheduler,
    outbox_job: OutboxJob
    ) -> Iterator[Scheduler]:
    try:
        scheduler.add_job(
            trigger=IntervalTrigger(seconds=10),
            job=outbox_job
            )
        yield scheduler
    finally:
        ...
        
        
def configure_created_mediator(
    mediator: IMediator, 
    move_courier_handler, 
    create_order_handler,
    assign_handler,
    get_busy_courier_handler,
    get_incompleted_orders_handler,
    order_finished_handler
    ) -> Iterator[IMediator]:
    try:
        mediator.register(MoveCourierCommand, move_courier_handler)
        mediator.register(AssigneCommand, assign_handler)
        mediator.register(CreateOrderCommand, create_order_handler)
        mediator.register(GetBusyCouriersQuery, get_busy_courier_handler)
        mediator.register(GetIncompletedOrdersQuery, get_incompleted_orders_handler)
        mediator.register(Event, order_finished_handler)
        yield mediator
    finally:
        ...
        
        
class DIContainer(BaseContainer):
    premediator = providers.Factory(
        Mediator
    )
    db_settings = providers.Factory(DBSettings)
    engine = providers.Factory(
        create_async_engine,
        db_settings.DB_URL,
        echo=True,
        )
    session = providers.Factory(
        async_sessionmaker,
        bind=engine, 
        expire_on_commit=False
        )
    dispatch_service = providers.Factory(DispatchService)
    courier_repository = providers.Factory(
        CourierRepository,
        session_maker=session,
        )
    order_repository = providers.Factory(
        OrderRepository,
        session_maker=session
        )
    uow = providers.Factory(
        UnitOfWork,
        session_maker=session
        )
    geo_grpc = providers.Factory(
        GeoGrpc,
        target="localhost:5004"
    )
    create_order_handler = providers.Factory(
        CreateOrderHandler, 
        repo=order_repository,
        geo_client=geo_grpc,
        uow=uow,
        )
    get_busy_courier_handler = providers.Factory(
        GetBusyCouriersHandler
        )
    get_incompleted_orders_handler = providers.Factory(
        GetIncompletedOrdersHandler
        )
    pre_message_bus = providers.Factory(
        KafkaBus,
        servers=[mq_settings.DESTINATION]
    )
    kafka_bus = providers.Resource(
        configure_created_message_bus,
        pre_message_bus.cast
    )
    order_finished_handler = providers.Factory(
        OrderFinishedHandler,
        message_bus=kafka_bus
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
        configure_created_mediator,
        premediator.cast,
        move_courier_handler.cast,
        create_order_handler.cast,
        assign_handler.cast,
        get_busy_courier_handler.cast,
        get_incompleted_orders_handler.cast,
        order_finished_handler.cast,
        )
    outbox_job = providers.Factory(
        OutboxJob,
        mediator=mediator,
        session_maker=session
    )
    prescheduler = providers.Factory(
        Scheduler
    )
    scheduler = providers.Resource(
        configure_scheduler,
        prescheduler.cast,
        outbox_job.cast
    )