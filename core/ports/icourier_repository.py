from typing import Protocol
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.courier_aggregate.courier import Courier


class ICourierRepository(Protocol):
    
    async def get_courier(self, courier_id: UUID) -> Courier:
        ...
        
    async def update_courier(self, session: AsyncSession, courier: Courier) -> None:
        ...
        
    async def add_courier(self, session: AsyncSession, courier: Courier) -> None:
        ...
        
    async def get_free_couriers(self) -> list[Courier]:
        ...