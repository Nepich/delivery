from dataclasses import dataclass
from core.ports.imessage_bus import IMessageBus
from infrastructure.adapters.postgres.entities.event import Event


@dataclass(slots=True, frozen=True)
class OrderFinishedHandler:
    message_bus: IMessageBus
    
    async def handle(self, event: Event):
        await self.message_bus.publish(event=event)