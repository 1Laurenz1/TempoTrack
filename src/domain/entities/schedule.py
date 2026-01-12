from src.domain.value_objects.day_of_week import DayOfWeek
from src.domain.value_objects.schedule_types import ScheduleTypes
from src.domain.entities.schedule_items import ScheduleItems

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Optional, Tuple


@dataclass
class Schedule:
    """Domain entity representing a user-defined schedule."""

    user_id: int

    id: Optional[int] = None
    name: str = field(default_factory=str)
    description: Optional[str] = None
    type_schedule: ScheduleTypes = ScheduleTypes.DAILY

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def id_and_user_id(self) -> Tuple[int, int]:
        return (self.id, self.user_id)
    
    def is_item_active_on_date(
        self,
        item: "ScheduleItems",
        day: date,
    ) -> bool:
        if self.type_schedule == ScheduleTypes.DAILY:
            return True
        
        if self.type_schedule == ScheduleTypes.WEEKLY:
            if item.day_of_week is None:
                return False
            
            weekday_map = {
                0: DayOfWeek.MONDAY,
                1: DayOfWeek.TUESDAY,
                2: DayOfWeek.WEDNESDAY,
                3: DayOfWeek.THURSDAY,
                4: DayOfWeek.FRIDAY,
                5: DayOfWeek.SATURDAY,
                6: DayOfWeek.SUNDAY,
            }
            
            return weekday_map[day.weekday()] == item.day_of_week
        return False