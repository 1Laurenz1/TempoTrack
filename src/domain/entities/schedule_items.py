from src.domain.value_objects.day_of_week import DAY_OF_WEEK

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class ScheduleItems:
    """"Represents a scheduled action with its timings, metadata, and optional weekday."""
    id: Optional[int] = None
    schedule_id: int
    
    name: str = field(default_factory=str)
    description: Optional[str] = None
    
    day_of_week: Optional[DAY_OF_WEEK] = None
    
    time_start: datetime.time
    time_end: datetime.time
    
    created_at: datetime = field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=datetime.now(timezone.utc))
    
    
    @property
    def duration(self) -> bool:
        return datetime.combine(datetime.min, self.time_end) - datetime.combine(datetime.min, self.time_start)