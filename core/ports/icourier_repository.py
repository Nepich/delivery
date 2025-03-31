from typing import Protocol
from uuid import UUID

from core.domain.courier_aggregate.courier import Courier


class ICourierRepository(Protocol):
    
    async def get_courier(self, courier_id: UUID) -> Courier:
        ...
        
    async def update_courier(self, courier: Courier) -> None:
        ...
        
    async def add_courier(self, courier: Courier) -> None:
        ...
        
    async def get_free_couriers(self) -> list[Courier]:
        ...