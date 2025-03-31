from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload

from core.domain.courier_aggregate.courier import Courier
from core.domain.courier_aggregate.courier_status import CourierStatus
from core.domain.courier_aggregate.transport import Transport
from infrastructure.adapters.postgres.session import async_session
from infrastructure.adapters.postgres.mappings import courier_table, transport_table


class CourierRepository:
    
    async def get_courier(self, courier_id: UUID) -> Courier:
        async with async_session() as session:
            stmt = (
                select(Courier)
                .options(joinedload(Courier._transport))
                .where(courier_table.c.id == courier_id)
            )
            result = await session.execute(stmt)
            return result.scalar_one()
        
    async def update_courier(self, courier: Courier) -> None:
        async with async_session() as session:
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
            await session.commit()
        
    async def add_courier(self, courier: Courier) -> None:
        async with async_session() as session, session.begin():
            session.add_all([courier, courier.transport])
            await session.commit()
        
    async def get_free_couriers(self) -> list[Courier]:
        async with async_session() as session:
            stmt = (
                select(Courier)
                .options(joinedload(Courier._transport))
                .where(courier_table.c.status == CourierStatus.FREE)
            )
            result = await session.execute(stmt)
            return result.scalars().unique().all()