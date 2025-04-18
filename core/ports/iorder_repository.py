from typing import Protocol
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.order_aggregate.order import Order


class IOrderRepository(Protocol):
    
    async def get_order(self, order_id: UUID) -> Order:
        ...
        
    async def update_order(self, session: AsyncSession, order: Order) -> None:
        ...
        
    async def add_order(self, session: AsyncSession, order: Order) -> None:
        ...
        
    async def get_new_order(self) -> Order:
        ...
        
    async def get_assigned_orders(self) -> list[Order]:
        ...