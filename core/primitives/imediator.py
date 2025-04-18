from typing import Protocol

from core.primitives.icommand import Command
from core.primitives.icommand_handler import ICommandHandler
from core.primitives.idomain_event import DomainEvent
from core.primitives.idomain_event_handler import IDomainEventHandler


class IMediator(Protocol):
    async def register(
        self, 
        command: Command | DomainEvent, 
        handler: IDomainEventHandler | ICommandHandler
        ):
        ...
        
    async def notify(self, command):
        ...