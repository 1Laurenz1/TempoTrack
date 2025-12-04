from enum import Enum


class ScheduleTypes(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    
    
    @classmethod
    def from_str(cls, value: str):
        for item in cls:
            if item.value.upper() == value.upper():
                return item
        raise ValueError(f"Invalid ScheduleType: {value}")