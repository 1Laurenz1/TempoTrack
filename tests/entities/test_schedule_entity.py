import pytest
from datetime import datetime

from src.domain.entities.schedule import Schedule
from src.domain.value_objects.schedule_types import ScheduleTypes



def test_schedule_creation():
    schedule = Schedule(
        user_id=1,
        name="schedule_name",
        description="description",
    )
    
    assert schedule.user_id == 1
    assert schedule.name == "schedule_name"
    assert schedule.description == "description"
    assert schedule.type_schedule == ScheduleTypes.DAILY
    assert isinstance(schedule.created_at, datetime)
    assert isinstance(schedule.updated_at, datetime)
    
    
def test_schedule_id_and_user_id():
    schedule = Schedule(id=10, user_id=5)
    
    assert schedule.id_and_user_id() == (10, 5)