from dataclasses import dataclass

from typing import Optional

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