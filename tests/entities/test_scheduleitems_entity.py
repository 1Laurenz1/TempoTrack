import pytest
from datetime import datetime, time, timedelta

from src.domain.entities.schedule_items import ScheduleItems
from src.domain.value_objects.day_of_week import DayOfWeek


def test_scheduleitem_creation():
    schedule_item = ScheduleItems(
        schedule_id=1,
        name="Walk",
        time_start=time(9,0),
        time_end=time(10, 0),
        day_of_week=DayOfWeek.MONDAY
    )

    assert schedule_item.schedule_id == 1
    assert schedule_item.name == "Walk"
    assert schedule_item.time_start == time(9, 0)
    assert schedule_item.time_end == time(10, 0)
    assert schedule_item.day_of_week == DayOfWeek.MONDAY
    assert isinstance(schedule_item.created_at, datetime)
    assert isinstance(schedule_item.updated_at, datetime)
    

def test_schedule_item_duration():
    item = ScheduleItems(
        schedule_id=1,
        time_start=time(12, 0),
        time_end=time(14, 30),
    )

    assert item.duration == timedelta(hours=2, minutes=30)