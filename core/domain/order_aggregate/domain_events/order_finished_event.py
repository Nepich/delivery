from dataclasses import dataclass, field
from uuid import UUID, uuid4

from core.domain.order_aggregate.order_status import OrderStatus
from core.primitives.idomain_event import DomainEvent


@dataclass
class OrderFinished(DomainEvent):
    order_id: UUID
    status: OrderStatus