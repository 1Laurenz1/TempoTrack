from abc import ABC, abstractmethod

from src.domain.entities.schedule import Schedule

from typing import Optional


class ScheduleRepository(ABC):
    
    @abstractmethod
    async def create(self, schedule: Schedule) -> Optional[Schedule]:
        """Add a new schedule to the database. Returns the created schedule or None if failed"""
        ...
        
    @abstractmethod
    async def get_schedule_by_id(self, id: int) -> Optional[Schedule]:
        """Returns the schedule by id or None if not found"""
        ...
        
        
    @abstractmethod
    async def get_user_schedules(self, user_id: int) -> Optional[Schedule]:
        """Returns the number of user's schedules"""
        ...