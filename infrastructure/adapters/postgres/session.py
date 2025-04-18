from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from infrastructure.settings import settings


async_engine = create_async_engine(settings.DB_URL, echo=True)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)