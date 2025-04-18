import asyncio
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.primitives.imediator import IMediator
from infrastructure.adapters.postgres.entities.event import Event


@dataclass
class OutboxJob:
    mediator: IMediator
    session_maker: async_sessionmaker
        
    async def process(self):
        session = self.session_maker()
        events = await session.scalars(
            select(Event)
            .where(Event.processed_at == None)
            .order_by(Event.created_at)
            )
        
        for event in events:
            try:
                await self.mediator.notify(event)
                event.processed_at = datetime.now()
                session.add(event)
            except Exception:
                continue

        await session.commit()
