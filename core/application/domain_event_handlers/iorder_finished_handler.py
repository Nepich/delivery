from typing import Protocol


class IOrderFinishedHandler(Protocol):
    
    async def handle(self, event: any):
        ...