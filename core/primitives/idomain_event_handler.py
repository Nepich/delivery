from typing import Protocol

from core.primitives.idomain_event import IDomainEvent


class IDomainEventHandler(Protocol):
    
    async def handle(self, event: IDomainEvent):
        ...