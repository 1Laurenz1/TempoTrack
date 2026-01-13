from dataclasses import dataclass

from datetime import time
from typing import Optional

from src.domain.value_objects.day_of_week import DayOfWeek
from src.domain.value_objects.schedule_types import ScheduleTypes


@dataclass(slots=True)
class ScheduleCreateRequest:
    name: str
    type_schedule: ScheduleTypes = ScheduleTypes.DAILY
    description: Optional[str] = None

@dataclass(slots=True)
class ScheduleCreateResponse:
    id: int
    name: str
    type_schedule: ScheduleTypes = ScheduleTypes.DAILY
    
    description: Optional[str] = None
    
    
@dataclass
class SetMainScheduleRequest:
    schedule_id: int
  
@dataclass
class SetMainScheduleResponse:
    schedule_id: int
    schedule_name: int
    
    
@dataclass(slots=True)
class AddScheduleItemRequest:
    name: str
    time_start: time
    time_end: time
    description: Optional[str] = None
    day_of_week: Optional[DayOfWeek] = None
    
    
@dataclass(slots=True)
class AddScheduleItemResponse:
    name: str
    time_start: time
    time_end: time
    description: Optional[str] = None
    day_of_week: Optional[DayOfWeek] = None