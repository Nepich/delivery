from sqlalchemy import Column, ForeignKey, Integer, MetaData, Table, Enum, Uuid, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import registry, composite, relationship, DeclarativeBase

from core.domain.courier_aggregate.courier import Courier
from core.domain.courier_aggregate.courier_status import CourierStatus
from core.domain.courier_aggregate.transport import Transport
from core.domain.order_aggregate.order import Order
from core.domain.order_aggregate.order_status import OrderStatus
from core.domain.shared_kernel.location import Location


mapper_registry = registry()
metadata_obj = MetaData()

order_table = Table(
    "order",
    metadata_obj,
    Column("id", Uuid, primary_key=True),
    Column("location_x", Integer),
    Column("location_y", Integer),
    Column("status", Enum(OrderStatus)),
    Column("courier_id", Uuid, nullable=True),
)

courier_table = Table(
    "courier",
    metadata_obj,
    Column("id", Uuid, primary_key=True),
    Column("location_x", Integer),
    Column("location_y", Integer),
    Column("status", Enum(CourierStatus)),
    Column("name", String(100)),
)

transport_table = Table(
    "transport",
    metadata_obj,
    Column("id", Uuid, primary_key=True),
    Column("speed", Integer),
    Column("name", String(100)),
    Column("courier_id", Uuid, ForeignKey("courier.id")),
)


mapper_registry.map_imperatively(
    Order,
    order_table,
    properties={
        "_id": order_table.c.id,
        "_location": composite(Location, order_table.c.location_x, order_table.c.location_y),
        "_status": order_table.c.status,
        "_courier_id": order_table.c.status,
    },
)

mapper_registry.map_imperatively(
    Courier,
    courier_table,
    properties={
        "_id": courier_table.c.id,
        "_location": composite(Location, courier_table.c.location_x, courier_table.c.location_y),
        "_status": courier_table.c.status,
        "_transport": relationship(Transport, uselist=False)
    },
)

mapper_registry.map_imperatively(
    Transport,
    transport_table,
    properties={
        "_id": transport_table.c.id
    },
)