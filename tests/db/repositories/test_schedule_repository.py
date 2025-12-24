from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.schedule import Schedule
from src.domain.entities.user import User
from src.domain.value_objects.schedule_types import ScheduleTypes
from src.infrastructure.database.repositories.schedule_repository_impl import (
    ScheduleRepositoryImpl
)

import pytest

from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl


@pytest.mark.asyncio
async def test_schedule_creation_success(db_session: AsyncSession):
    schedule_repository = ScheduleRepositoryImpl(db_session)
    user_repository = UserRepositoryImpl(db_session)
    
    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=1,
        main_schedule=1
    )

    await user_repository.add(user)
    
    schedule = Schedule(
        user_id=1,
        id=1,
        name="test_name",
        description="First test schedule"
    )
    
    new_schedule = await schedule_repository.create(
        schedule
    )
    
    assert new_schedule.user_id == 1
    assert new_schedule.id == 1
    assert new_schedule.name == "test_name"
    assert new_schedule.description == "First test schedule"
    assert new_schedule.type_schedule == ScheduleTypes.DAILY
    assert isinstance(new_schedule.created_at, datetime)
    assert isinstance(new_schedule.updated_at, datetime)


@pytest.mark.asyncio
async def test_get_schedule_by_id_success(db_session: AsyncSession):
    schedule_repository = ScheduleRepositoryImpl(db_session)
    user_repository = UserRepositoryImpl(db_session)
    
    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=1,
        main_schedule=1
    )

    await user_repository.add(user)
    
    schedule = Schedule(
        user_id=1,
        id=1,
        name="test_name",
        description="First test schedule"
    )
    
    await schedule_repository.create(
        schedule
    )
    
    get_schedule = await schedule_repository.get_schedule_by_id(1)
    
    assert get_schedule is not None
    
    
@pytest.mark.asyncio
async def test_get_schedule_by_id_not_found(db_session: AsyncSession):
    schedule_repository = ScheduleRepositoryImpl(db_session)
    
    get_schedule = await schedule_repository.get_schedule_by_id(3)
    
    assert get_schedule is None