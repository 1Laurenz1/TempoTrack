from dataclasses import dataclass

@dataclass
class SetMainScheduleRequest:
    schedule_id: int
  
    
@dataclass
class SetMainScheduleResponse:
    schedule_id: int
    schedule_name: int