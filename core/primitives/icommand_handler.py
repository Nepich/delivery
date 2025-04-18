from typing import Any, Protocol

from core.primitives.icommand import Command



class ICommandHandler(Protocol):
    
    async def handle(self, command: Command):
        ...