from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from core.domain.order_aggregate.order import Order
from core.domain.order_aggregate.order_status import OrderStatus
from infrastructure.adapters.postgres.mappings import order_table


@dataclass
class OrderRepository:
    session_maker: async_sessionmaker
    
    async def get_order(self, order_id: UUID) -> Order:
        async with self.session_maker() as session:
            stmt = (
                select(Order)
                .where(order_table.c.id == order_id)
            )
            result = await session.execute(stmt)
            return result.scalar_one()
        
    async def update_order(self, session: AsyncSession, order: Order) -> None:
        stmt = (
            update(order_table)
            .where(order_table.c.id == order.id)
            .values(
                id=order.id,
                location_x=order.location.x,
                location_y=order.location.y,
                status=order.status,
                courier_id=order.courier_id
                )
        )
        await session.execute(stmt)
        
    async def add_order(self, session: AsyncSession, order: Order) -> None:
        session.add(order)
        
    async def get_new_order(self) -> Order:
        async with self.session_maker() as session:
            stmt = (
                select(Order)
                .where(order_table.c.status == OrderStatus.CREATED)
            )
            result = await session.execute(stmt)
            return result.scalars().unique().first()
        
    async def get_assigned_orders(self) -> list[Order]:
        async with self.session_maker() as session:
            stmt = (
                select(Order)
                .where(order_table.c.status == OrderStatus.ASSIGNED)
            )
            result = await session.execute(stmt)
            return result.scalars().unique().all()