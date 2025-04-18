from core.primitives.icommand import Command
from core.primitives.icommand_handler import ICommandHandler
from core.primitives.idomain_event import DomainEvent
from core.primitives.idomain_event_handler import IDomainEventHandler


class Mediator:
    
    def __init__(self):
        self.__handlers = {}
    
    def register(
        self, 
        command: Command | DomainEvent, 
        handler: IDomainEventHandler | ICommandHandler
        ):
        self.__handlers[command] = handler
        
    async def notify(self, command):
        handler = self.__handlers[command.__class__]
        await handler.handle(command)