from abc import ABC, abstractmethod

from src.domain.entities.schedule_items import ScheduleItems

from typing import List


class ScheduleItemsRepository(ABC):
    @abstractmethod
    async def add(self, schedule_item: List[ScheduleItems], user_id: int) -> List[ScheduleItems]:
        """Adds one or more schedule elements to the database"""
        ...
        
        
    @abstractmethod
    async def get_items_by_schedule_id(
        self,
        schedule_id: int,
        user_id: int
    ) -> List[ScheduleItems]:
        """Returns all items that are in the schedule"""
        ...