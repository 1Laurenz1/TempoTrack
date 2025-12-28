from src.domain.value_objects.day_of_week import DayOfWeek
from dataclasses import dataclass, field
from datetime import datetime, timezone, time
from typing import Optional


@dataclass
class ScheduleItems:
    """Represents a scheduled action with its timings, metadata, and optional weekday."""

    schedule_id: int
    user_id: int
    time_start: time
    time_end: time

    id: Optional[int] = None
    name: str = field(default_factory=str)
    description: Optional[str] = None
    day_of_week: Optional[DayOfWeek] = None

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def duration(self):
        return (
            datetime.combine(datetime.min, self.time_end) - datetime.combine(datetime.min, self.time_start)
        )
