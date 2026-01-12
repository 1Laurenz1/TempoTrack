import pytest
from datetime import datetime, time, timedelta, timezone

from src.application.usecases.prepare_schedule_notification import (
    PrepareScheduleNotificationUseCase
)

from src.application.exceptions.schedule_notifications import (
    InvalidNotificationStatusError
)

from src.domain.entities.schedule_notification import ScheduleNotification
from src.domain.value_objects.notification_status import ScheduleNotificationStatus


class FakeScheduleNotificationRepo:
    def __init__(self, notifications):
        self.notifications = {n.id: n for n in notifications}

    async def get_by_id(self, notification_id: int):
        return self.notifications.get(notification_id)



@pytest.mark.asyncio
async def test_prepare_notification_returns_none_if_not_found():
    repo = FakeScheduleNotificationRepo(notifications=[])

    usecase = PrepareScheduleNotificationUseCase(notification_repo=repo)

    result = await usecase.execute(notification_id=1)

    assert result is None


@pytest.mark.asyncio
async def test_prepare_notification_raises_if_status_not_pending():
    notification = ScheduleNotification(
        id=1,
        user_id=1,
        schedule_item_id=1,
        time_start=time(12, 0),
        time_end=time(13, 0),
        payload="Test",
        status=ScheduleNotificationStatus.SENT,
    )

    repo = FakeScheduleNotificationRepo([notification])
    usecase = PrepareScheduleNotificationUseCase(repo)

    with pytest.raises(InvalidNotificationStatusError):
        await usecase.execute(notification_id=1)


@pytest.mark.asyncio
async def test_prepare_notification_returns_positive_delay_for_future_time():
    now = datetime.now(timezone.utc)
    future_time = (now + timedelta(minutes=10)).time()

    notification = ScheduleNotification(
        id=1,
        user_id=1,
        schedule_item_id=1,
        time_start=future_time,
        time_end=time(13, 0),
        payload="Test",
        status=ScheduleNotificationStatus.PENDING,
    )

    repo = FakeScheduleNotificationRepo([notification])
    usecase = PrepareScheduleNotificationUseCase(repo)

    delay = await usecase.execute(notification_id=1)

    assert delay > 0


@pytest.mark.asyncio
async def test_prepare_notification_returns_zero_delay_for_past_time():
    now = datetime.now(timezone.utc)
    past_time = (now - timedelta(minutes=10)).time()

    notification = ScheduleNotification(
        id=1,
        user_id=1,
        schedule_item_id=1,
        time_start=past_time,
        time_end=time(13, 0),
        payload="Test",
        status=ScheduleNotificationStatus.PENDING,
    )

    repo = FakeScheduleNotificationRepo([notification])
    usecase = PrepareScheduleNotificationUseCase(repo)

    delay = await usecase.execute(notification_id=1)

    assert delay == 0
