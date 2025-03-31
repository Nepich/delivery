from uuid import UUID

from sqlalchemy import insert, select, update

from core.domain.order_aggregate.order import Order
from core.domain.order_aggregate.order_status import OrderStatus
from infrastructure.adapters.postgres.session import async_session
from infrastructure.adapters.postgres.mappings import order_table



class OrderRepository:
    
    async def get_order(self, order_id: UUID) -> Order:
        async with async_session() as session:
            stmt = (
                select(Order)
                .where(order_table.c.id == order_id)
            )
            result = await session.execute(stmt)
            return result.scalar_one()
        
    async def update_order(self, order: Order) -> None:
        async with async_session() as session:
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
            await session.commit()
        
    async def add_order(self, order: Order) -> None:
        async with async_session() as session, session.begin():
            session.add(order)
            await session.commit()
        
    async def get_new_order(self) -> Order:
        async with async_session() as session:
            stmt = (
                select(Order)
                .where(order_table.c.status == OrderStatus.CREATED)
            )
            result = await session.execute(stmt)
            return result.scalars().unique().first()
        
    async def get_assigned_orders(self) -> list[Order]:
        async with async_session() as session:
            stmt = (
                select(Order)
                .where(order_table.c.status == OrderStatus.ASSIGNED)
            )
            result = await session.execute(stmt)
            return result.scalars().unique().all()