from src.domain.repositories.schedule_items import ScheduleItemsRepository
from src.domain.repositories.schedule_repository import ScheduleRepository
from src.domain.repositories.schedule_notifications_repository import (
    ScheduleNotificationRepository
)

from src.domain.entities.schedule_notification import ScheduleNotification
from src.domain.value_objects.notification_status import ScheduleNotificationStatus

from src.application.exceptions.schedule import MainScheduleNotSetError
from src.application.exceptions.schedule_items import NoScheduleItemsError

from datetime import datetime, timezone
from typing import List


class GenerateScheduleNotificationsUseCase:
    def __init__(
        self,
        schedule_items_repo: ScheduleItemsRepository,
        schedule_repo: ScheduleRepository,
        schedule_notification_repo: ScheduleNotificationRepository,
    ):
        self.schedule_items_repo = schedule_items_repo
        self.schedule_repo = schedule_repo
        self.schedule_notification_repo = schedule_notification_repo

        
    async def execute(
        self,
        user_id: int,
    ) -> bool:
        main_schedule = await self.schedule_repo.get_user_main_schedule(user_id)
        
        if not main_schedule:
            raise MainScheduleNotSetError("User has not selected a main schedule")
        
        schedule_items = await self.schedule_items_repo.get_items_by_schedule_id(
            schedule_id=main_schedule.id,
            user_id=user_id
        )
        
        if not schedule_items:
            raise NoScheduleItemsError("Failed to retrieve schedule items — it is empty.")
        
        today = datetime.now(timezone.utc).date()
        
        notifications: List[ScheduleNotification] = []
        
        for item in schedule_items:
            if main_schedule.is_item_active_on_date(item, today):
                notifications.append(
                    ScheduleNotification(
                        user_id=user_id,
                        schedule_item_id=item.id,
                        time_start=item.time_start,
                        time_end=item.time_end,
                        payload=item.name,
                        status=ScheduleNotificationStatus.PENDING,    
                    )                    
                )
        
        if notifications:
            await self.schedule_notification_repo.add_many(notifications)
            return True