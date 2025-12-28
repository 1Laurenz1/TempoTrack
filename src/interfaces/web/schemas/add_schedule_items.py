from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel

from src.domain.value_objects.day_of_week import DayOfWeek



class AddScheduleItemRequest(BaseModel):
    name: str
    time_start: time
    time_end: time
    description: Optional[str] = None
    day_of_week: Optional[DayOfWeek] = None
    
    
class AddScheduleItemResponse(BaseModel):
    name: str
    time_start: time
    time_end: time
    description: Optional[str] = None
    day_of_week: Optional[DayOfWeek] = None