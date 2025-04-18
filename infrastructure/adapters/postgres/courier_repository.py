from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from core.domain.courier_aggregate.courier import Courier
from core.domain.courier_aggregate.courier_status import CourierStatus
from infrastructure.adapters.postgres.mappings import courier_table


@dataclass
class CourierRepository:
    session_maker: async_sessionmaker
    
    async def get_courier(self, courier_id: UUID) -> Courier:
        async with self.session_maker() as session:
            stmt = (
                select(Courier)
                .options(joinedload(Courier._transport))
                .where(courier_table.c.id == courier_id)
            )
            result = await session.execute(stmt)
            return result.scalar_one()
        
    async def update_courier(self, session: AsyncSession, courier: Courier) -> None:
        stmt = (
            update(courier_table)
            .where(courier_table.c.id == courier.id)
            .values(
                location_x = courier.location.x,
                location_y = courier.location.y,
                status = courier.status
                )
        )
        await session.execute(stmt)
        
    async def add_courier(self, session: AsyncSession, courier: Courier) -> None:
        async with self.session_maker()() as session, session.begin():
            session.add_all([courier, courier.transport])
            await session.commit()
        
    async def get_free_couriers(self) -> list[Courier]:
        async with self.session_maker()() as session:
            stmt = (
                select(Courier)
                .options(joinedload(Courier._transport))
                .where(courier_table.c.status == CourierStatus.FREE)
            )
            result = await session.execute(stmt)
            return result.scalars().unique().all()