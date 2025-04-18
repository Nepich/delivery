from contextlib import asynccontextmanager
from dataclasses import dataclass
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from infrastructure.adapters.postgres.mappings import event_table


@dataclass
class UnitOfWork:
    session_maker: async_sessionmaker
    
    @asynccontextmanager
    async def __call__(self):
        session: AsyncSession = self.session_maker()
        try:
            yield session
            await session.flush()
            await self.__save_events_in_outbox(session=session)
            await session.commit()
        except Exception as ex:
            print(ex)
            await session.rollback()
        finally:
            await session.close()
    
    @staticmethod
    async def __save_events_in_outbox(session: AsyncSession):
        registry = session.identity_map.values()
        events = []

        for aggregate in registry:
            if aggregate.events:
                events.extend([event.as_dict() for event in aggregate.events])
        
        if events:
            stmt = insert(event_table).values(events)
            await session.execute(stmt)