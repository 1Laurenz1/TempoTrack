from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)

from src.infrastructure.config.config_reader import settings
from src.common.logging.logger_main import logger

from contextlib import asynccontextmanager
from typing import AsyncGenerator


class Base(AsyncAttrs, DeclarativeBase):
    ...


engine = create_async_engine(
    url=settings.DATABASE_URL.get_secret_value(), echo=True
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=True,
    autoflush=False,
    class_=AsyncSession
)


# @asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.info(f"The database query failed and returned an error: {e}")
            raise
        finally:
            await session.close()