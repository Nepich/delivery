from dataclasses import dataclass, field
from uuid import UUID, uuid4

from core.domain.order_aggregate.order_status import OrderStatus


@dataclass
class OrderFinishedEvent:
    order_id: UUID
    status: OrderStatus
    id: UUID = field(default_factory=uuid4)