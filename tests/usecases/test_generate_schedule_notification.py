import pytest
from datetime import time, datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecases.generate_schedule_notifications import (
    GenerateScheduleNotificationsUseCase
)

from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.database.repositories.schedule_repository_impl import ScheduleRepositoryImpl
from src.infrastructure.database.repositories.schedule_items_repository_impl import ScheduleItemsRepositoryImpl
from src.infrastructure.database.repositories.schedule_notification import (
    ScheduleNotificationRepositoryImpl
)

from src.domain.entities.user import User
from src.domain.entities.schedule import Schedule
from src.domain.entities.schedule_items import ScheduleItems
from src.domain.value_objects.day_of_week import DayOfWeek
from src.domain.value_objects.schedule_types import ScheduleTypes
from src.domain.value_objects.notification_status import ScheduleNotificationStatus


@pytest.mark.asyncio
async def test_generate_schedule_notifications_success(db_session: AsyncSession):
    user_repo = UserRepositoryImpl(db_session)
    schedule_repo = ScheduleRepositoryImpl(db_session)
    items_repo = ScheduleItemsRepositoryImpl(db_session)
    notification_repo = ScheduleNotificationRepositoryImpl(db_session)

    usecase = GenerateScheduleNotificationsUseCase(
        schedule_items_repo=items_repo,
        schedule_repo=schedule_repo,
        schedule_notification_repo=notification_repo,
    )

    # --- user ---
    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        main_schedule=1
    )
    created_user = await user_repo.add(user)

    # --- schedule ---
    schedule = Schedule(
        user_id=created_user.id,
        name="Main schedule",
        description="Test schedule",
        type_schedule=ScheduleTypes.DAILY,
    )
    created_schedule = await schedule_repo.create(schedule)

    # --- schedule item (daily) ---
    item = ScheduleItems(
        schedule_id=created_schedule.id,
        user_id=created_user.id,
        time_start=time(hour=8, minute=0),
        time_end=time(hour=9, minute=0),
        name="Morning routine",
        day_of_week=None,  # DAILY
    )

    await items_repo.add([item], user_id=created_user.id)

    # --- execute ---
    result = await usecase.execute(user_id=created_user.id)

    # --- assert ---
    notifications = await notification_repo.get_by_user_id(created_user.id)

    assert result is True
    assert len(notifications) == 1
    # assert notifications[0].status == ScheduleNotificationStatus.PENDING
    assert notifications[0].schedule_item_id is not None
