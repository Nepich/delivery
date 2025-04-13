from typing import Any, Protocol


class ICommandHandler(Protocol):
    
    async def handle(self, command: Any):
        ...