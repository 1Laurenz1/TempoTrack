from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.session import Base
from src.infrastructure.config.config_reader import settings

from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.models.schedule import ScheduleModel
from src.infrastructure.database.models.schedule_items import ScheduleItemsModel
from src.infrastructure.database.models.refresh_token import RefreshTokenModel
from src.infrastructure.database.models.schedule_notification import (
    ScheduleNotificationModel
)

import pytest_asyncio

import asyncio


@pytest_asyncio.fixture
async def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
    


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(
        settings.TEST_DATABASE_URL.get_secret_value(),
        echo=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    yield engine
    
    await engine.dispose()
    
    
@pytest_asyncio.fixture
async def db_session(test_engine):
    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e 
        finally:
            await session.close()