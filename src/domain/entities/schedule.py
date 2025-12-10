from src.domain.value_objects.schedule_types import ScheduleTypes
from dataclasses import dataclass, field
from datetime import datetime, timezone
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