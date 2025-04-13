from typing import Any, Protocol


class IMessageBus(Protocol):
    
    async def publish(self, topic: str, event: Any):
        ...