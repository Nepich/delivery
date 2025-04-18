from typing import Protocol

from core.primitives.idomain_event import DomainEvent


class IDomainEventHandler(Protocol):
    
    async def handle(self, event: DomainEvent):
        ...