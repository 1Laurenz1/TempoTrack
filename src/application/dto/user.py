from dataclasses import dataclass

from datetime import datetime
from typing import Optional

from src.domain.value_objects.schedule_types import ScheduleTypes


@dataclass(slots=True)
class UserMeResponse():
    id: int
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    tg_username: str | None
    created_at: datetime
    
    
@dataclass(slots=True)
class UserMeSchedulesResponse():
    id: int
    name: str
    type_schedule: ScheduleTypes
    
    created_at: datetime
    updated_at: datetime
    
    description: Optional[str]