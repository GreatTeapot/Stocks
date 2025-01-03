from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine_async = create_async_engine(settings.db.async_database_url)
async_session_maker = async_sessionmaker(engine_async)

engine_sync = create_engine(settings.db.sync_database_url)
sync_session_maker = sessionmaker(engine_sync)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
