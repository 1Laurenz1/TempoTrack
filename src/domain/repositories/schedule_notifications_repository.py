from abc import ABC, abstractmethod

from src.domain.entities.schedule_notification import ScheduleNotification

from typing import Optional


class ScheduledNotificationRepository(ABC):
    @abstractmethod
    async def add(
        self,
        notification: ScheduleNotification
    ) -> Optional[ScheduleNotification]:
        """Adds a new object for notification"""
        ...