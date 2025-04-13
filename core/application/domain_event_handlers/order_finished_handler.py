from dataclasses import dataclass
from core.domain.order_aggregate.domain_events.order_finished_event import OrderFinishedEvent
from core.ports.imessage_bus import IMessageBus


@dataclass(slots=True, frozen=True)
class OrderFinishedHandler:
    message_bus: IMessageBus
    
    async def handle(self, event: any):
        if isinstance(event, OrderFinishedEvent):
            self.message_bus.publish(event=event)