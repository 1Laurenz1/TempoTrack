from datetime import datetime, time, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.value_objects.day_of_week import DayOfWeek
from src.infrastructure.database.models.schedule_items import ScheduleItemsModel
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.models.schedule import ScheduleModel

from src.domain.value_objects.schedule_types import ScheduleTypes

import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_scheduleitems_model(db_session: AsyncSession):
    user = UserModel(
        id=10,
        username="test",
        email="test@example.com",
        password="123"
    )
    db_session.add(user)

    schedule = ScheduleModel(
        name="Daily Routine",
        description="Morning tasks",
        type_schedule=ScheduleTypes.DAILY,
        user_id=user.id
    )
    db_session.add(schedule)
    await db_session.commit()
    
    schedule_item = ScheduleItemsModel(
        schedule_id=1,
        name="Workload(first block)",
        description="2 hours of hard work",
        day_of_week=DayOfWeek.MONDAY,
        time_start=time(10,0),
        time_end=time(12, 0),
        user_id=10
    )
    
    db_session.add(schedule_item)
    await db_session.commit()
    await db_session.refresh(schedule_item)
    
    assert schedule_item.id is not None
    assert schedule_item.name == "Workload(first block)"
    assert schedule_item.description == "2 hours of hard work"
    assert schedule_item.day_of_week == DayOfWeek.MONDAY
    assert schedule_item.time_start == time(10, 0)
    assert schedule_item.time_end == time(12, 0)
    assert isinstance(schedule_item.created_at, datetime)
    assert isinstance(schedule_item.updated_at, datetime)
    

def test_schedule_item_duration():
    item = ScheduleItemsModel(
        schedule_id=1,
        time_start=time(12, 0),
        time_end=time(14, 30),
    )

    assert item.duration == timedelta(hours=2, minutes=30)