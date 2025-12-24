from typing import Optional
from pydantic import BaseModel

from src.domain.value_objects.schedule_types import ScheduleTypes


class ScheduleCreateRequest(BaseModel):
    name: str
    type_schedule: ScheduleTypes = ScheduleTypes.DAILY
    description: Optional[str] = None
    
    
class ScheduleCreateResponse(BaseModel):
    id: int
    name: str
    type_schedule: ScheduleTypes = ScheduleTypes.DAILY
    
    description: Optional[str] = None