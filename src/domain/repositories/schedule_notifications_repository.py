from abc import ABC, abstractmethod

from src.domain.entities.schedule_notification import ScheduleNotification

from typing import Optional, List


class ScheduleNotificationRepository(ABC):
    @abstractmethod
    async def add(
        self,
        notification: ScheduleNotification
    ) -> Optional[ScheduleNotification]:
        """Adds a new object for notification"""
        ...
        
        
    @abstractmethod
    async def add_many(
        self,
        notifications: List[ScheduleNotification]
    ) -> List[ScheduleNotification]:
        """Adds several objects for notifications"""
        ...