from typing import Optional
from pydantic import BaseModel

from src.domain.value_objects.schedule_types import ScheduleTypes


class ScheduleCreateRequest:
    name: str
    type_schedule: ScheduleTypes = ScheduleTypes.DAILY
    desciption: Optional[str] = None
    
    
class ScheduleCreateResponse:
    id: int
    name: str
    type_schedule: ScheduleTypes = ScheduleTypes.DAILY
    
    description: Optional[str] = None