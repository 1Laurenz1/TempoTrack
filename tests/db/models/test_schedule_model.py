from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.schedule import ScheduleModel
from src.infrastructure.database.models.user import UserModel
from src.domain.value_objects.schedule_types import ScheduleTypes

import pytest
import pytest_asyncio
from src.application.services.password_service import PasswordService


@pytest.mark.asyncio
async def test_schedule_creation(db_session: AsyncSession):
    password_manager = PasswordService()
    user = UserModel(
        username="Alice",
        email="alice@example.com",
        password=password_manager.hash("secret")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    schedule = ScheduleModel(
        name="Daily Routine",
        description="Morning tasks",
        type_schedule=ScheduleTypes.DAILY,
        user_id=user.id
    )

    db_session.add(schedule)
    await db_session.commit()
    await db_session.refresh(schedule)

    assert schedule.id is not None
    assert schedule.name == "Daily Routine"
    assert schedule.description == "Morning tasks"
    assert schedule.type_schedule == ScheduleTypes.DAILY
    assert schedule.user_id == user.id
    assert schedule.user.username == "Alice"