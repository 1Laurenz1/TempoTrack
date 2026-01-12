import pytest
from datetime import date, time, datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.exceptions.schedule import MainScheduleNotSetError
from src.application.exceptions.schedule_items import NoScheduleItemsError
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

    schedule = Schedule(
        user_id=created_user.id,
        name="Main schedule",
        description="Test schedule",
        type_schedule=ScheduleTypes.DAILY,
    )
    created_schedule = await schedule_repo.create(schedule)

    item = ScheduleItems(
        schedule_id=created_schedule.id,
        user_id=created_user.id,
        time_start=time(hour=8, minute=0),
        time_end=time(hour=9, minute=0),
        name="Morning routine",
        day_of_week=None,  # DAILY
    )

    await items_repo.add([item], user_id=created_user.id)

    result = await usecase.execute(user_id=created_user.id)

    notifications = await notification_repo.get_by_user_id(created_user.id)

    assert result is True
    assert len(notifications) == 1
    assert notifications[0].status == ScheduleNotificationStatus.PENDING
    assert notifications[0].schedule_item_id is not None
    
    
@pytest.mark.asyncio
async def test_generate_notifications_no_main_schedule(db_session: AsyncSession):
    user_repo = UserRepositoryImpl(db_session)
    items_repo = ScheduleItemsRepositoryImpl(db_session)
    schedule_repo = ScheduleRepositoryImpl(db_session)
    notification_repo = ScheduleNotificationRepositoryImpl(db_session)

    usecase = GenerateScheduleNotificationsUseCase(
        schedule_items_repo=items_repo,
        schedule_repo=schedule_repo,
        schedule_notification_repo=notification_repo,
    )

    user = User(
        username="no_schedule",
        email="no_schedule@example.com",
        password=b"hashed",
        first_name="No",
        last_name="Schedule",
        tg_username="noschedule",
        telegram_id=111222333,
    )
    created_user = await user_repo.add(user)

    with pytest.raises(MainScheduleNotSetError):
        await usecase.execute(user_id=created_user.id)
        

@pytest.mark.asyncio
async def test_generate_notifications_no_schedule_items(db_session: AsyncSession):
    user_repo = UserRepositoryImpl(db_session)
    schedule_repo = ScheduleRepositoryImpl(db_session)
    items_repo = ScheduleItemsRepositoryImpl(db_session)
    notification_repo = ScheduleNotificationRepositoryImpl(db_session)

    usecase = GenerateScheduleNotificationsUseCase(
        schedule_items_repo=items_repo,
        schedule_repo=schedule_repo,
        schedule_notification_repo=notification_repo,
    )

    user = User(
        username="empty_items",
        email="empty@example.com",
        password=b"hashed",
        first_name="Empty",
        last_name="Items",
        tg_username="empty_items",
        telegram_id=999888777,
        main_schedule=1
    )
    created_user = await user_repo.add(user)

    schedule = Schedule(
        user_id=created_user.id,
        name="Empty schedule",
        type_schedule=ScheduleTypes.DAILY,
    )
    await schedule_repo.create(schedule)

    with pytest.raises(NoScheduleItemsError):
        await usecase.execute(user_id=created_user.id)
        
        
        
@pytest.mark.asyncio
async def test_generate_notifications_respects_item_schedule(db_session: AsyncSession):
    user_repo = UserRepositoryImpl(db_session)
    schedule_repo = ScheduleRepositoryImpl(db_session)
    items_repo = ScheduleItemsRepositoryImpl(db_session)
    notif_repo = ScheduleNotificationRepositoryImpl(db_session)

    usecase = GenerateScheduleNotificationsUseCase(
        schedule_items_repo=items_repo,
        schedule_repo=schedule_repo,
        schedule_notification_repo=notif_repo,
    )

    user = User(
        username="alice",
        email="alice@example.com",
        password=b"hashed",
        first_name="Alice",
        last_name="Liddell",
        tg_username="alice_tg",
        telegram_id=987654321,
        main_schedule=1
    )
    created_user = await user_repo.add(user)

    schedule = Schedule(
        user_id=created_user.id,
        name="Weekly schedule",
        type_schedule=ScheduleTypes.WEEKLY,
    )
    created_schedule = await schedule_repo.create(schedule)

    weekday_today = date.today().weekday()
    day_enum = list(DayOfWeek)[weekday_today]  # map int -> DayOfWeek Enum

    active_item = ScheduleItems(
        schedule_id=created_schedule.id,
        user_id=created_user.id,
        time_start=time(8, 0),
        time_end=time(9, 0),
        name="Active Item",
        day_of_week=day_enum,
    )

    inactive_item = ScheduleItems(
        schedule_id=created_schedule.id,
        user_id=created_user.id,
        time_start=time(10, 0),
        time_end=time(11, 0),
        name="Inactive Item",
        day_of_week=DayOfWeek.MONDAY if day_enum != DayOfWeek.MONDAY else DayOfWeek.TUESDAY,
    )

    created_items = await items_repo.add([active_item, inactive_item], user_id=created_user.id)
    active_item, inactive_item = created_items

    result = await usecase.execute(user_id=created_user.id)

    notifications = await notif_repo.get_by_user_id(created_user.id)

    assert result is True
    assert len(notifications) == 1
    assert notifications[0].schedule_item_id == active_item.id
    assert notifications[0].time_start == active_item.time_start
    assert notifications[0].time_end == active_item.time_end