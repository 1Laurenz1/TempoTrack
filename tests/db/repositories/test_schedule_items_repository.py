from datetime import datetime, time, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.domain.entities.schedule import Schedule
from src.domain.entities.user import User
from src.domain.entities.schedule_items import ScheduleItems

from src.domain.value_objects.day_of_week import DayOfWeek
from src.infrastructure.database.models.schedule_items import ScheduleItemsModel
from src.infrastructure.database.repositories.schedule_items_repository_impl import (
    ScheduleItemsRepositoryImpl
)
from src.infrastructure.database.repositories.schedule_repository_impl import ScheduleRepositoryImpl
from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl

import pytest
import asyncio


@pytest.mark.asyncio
async def test_add_user_schedule_item_success(db_session: AsyncSession):
    user_repo = UserRepositoryImpl(db_session)
    schedule_repo = ScheduleRepositoryImpl(db_session)
    item_repo = ScheduleItemsRepositoryImpl(db_session)
    
    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789
    )
    created_user = await user_repo.add(user)
    
    schedule = Schedule(
        user_id=created_user.id,
        name="test_name",
        description="First test schedule"
    )
    created_schedule = await schedule_repo.create(schedule)
    
    schedule_item = ScheduleItems(
        schedule_id=created_schedule.id,
        time_start=time(hour=8, minute=30),
        time_end=time(hour=9, minute=0),
        name="WAKE UP",
        day_of_week=DayOfWeek.MONDAY
    )
    
    created_items = await item_repo.add([schedule_item], user_id=created_user.id)
    
    assert created_user.id is not None
    assert created_schedule.id is not None
    assert len(created_items) == 1
    assert created_items[0].name == "WAKE UP"



@pytest.mark.asyncio
async def test_add_some_user_schedule_item_success(db_session: AsyncSession):
    user_repo = UserRepositoryImpl(db_session)
    schedule_repo = ScheduleRepositoryImpl(db_session)
    item_repo = ScheduleItemsRepositoryImpl(db_session)
    
    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789
    )
    created_user = await user_repo.add(user)
    
    schedule = Schedule(
        user_id=created_user.id,
        name="test_name",
        description="First test schedule"
    )
    created_schedule = await schedule_repo.create(schedule)
    
    schedule_item1 = ScheduleItems(
        schedule_id=created_schedule.id,
        time_start=time(hour=8, minute=30),
        time_end=time(hour=9, minute=0),
        name="WAKE UP",
        day_of_week=DayOfWeek.MONDAY
    )
    
    schedule_item2 = ScheduleItems(
        schedule_id=created_schedule.id,
        time_start=time(hour=9, minute=0),
        time_end=time(hour=9, minute=30),
        name="BREAKFAST",
        day_of_week=DayOfWeek.MONDAY
    )
    
    created_items = await item_repo.add([schedule_item1, schedule_item2], user_id=created_user.id)
    
    assert created_user.id is not None
    assert created_schedule.id is not None
    assert len(created_items) == 2
    assert created_items[0].name == "WAKE UP"
    assert created_items[1].name == "BREAKFAST"