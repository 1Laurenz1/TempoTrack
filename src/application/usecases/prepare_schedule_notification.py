from src.application.ports.telegram_sender import TelegramSender
from src.application.exceptions.schedule_notifications import (
    InvalidNotificationStatusError,
)

from src.domain.repositories.schedule_notifications_repository import (
    ScheduleNotificationRepository
)
from src.domain.value_objects.notification_status import (
    ScheduleNotificationStatus
)

from datetime import datetime, timezone


class PrepareScheduleNotificationUseCase:
    def __init__(
        self,
        notification_repo: ScheduleNotificationRepository,
    ):
        self.notification_repo = notification_repo
        
    
    async def execute(
        self,
        notification_id: int,
    ) -> int:
        notification = await self.notification_repo.get_by_id(notification_id)
        
        if not notification:
            return
        
        if notification.status != ScheduleNotificationStatus.PENDING:
            raise InvalidNotificationStatusError(
                f"Notification {notification.id} is not pending, current status: {notification.status}"
            )
            
        now = datetime.now(timezone.utc)
        
        notification_dt = datetime.combine(
            date=now.date(),
            time=notification.time_start,
            tzinfo=timezone.utc,
        )
        
        delay = (notification_dt - now).total_seconds()
        
        if delay < 0:
            delay = 0
        
        return delay