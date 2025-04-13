from typing import Protocol

from core.primitives.icommand import ICommand
from core.primitives.icommand_handler import ICommandHandler
from core.primitives.idomain_event import IDomainEvent
from core.primitives.idomain_event_handler import IDomainEventHandler


class IMediator(Protocol):
    async def register(
        self, 
        command: ICommand | IDomainEvent, 
        handler: IDomainEventHandler | ICommandHandler
        ):
        ...
        
    async def notify(self, command):
        ...