from sqlalchemy import (
    Integer,
    String,
    BigInteger,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM

from src.domain.entities.schedule_items import ScheduleItems
from src.domain.value_objects.day_of_week import DayOfWeek

from src.infrastructure.database.session import Base
from src.infrastructure.database.mixins.time_stamp_mixin import TimeStampMixin

from src.domain.value_objects.schedule_types import ScheduleTypes

from datetime import date
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from .user import UserModel
    from .schedule_items import ScheduleItemsModel


class ScheduleModel(Base, TimeStampMixin):
    __tablename__ = 'schedules'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True
    )
    description: Mapped[str] = mapped_column(
        String(512),
        nullable=True
    )
    type_schedule: Mapped[ScheduleTypes] = mapped_column(
        ENUM(
            ScheduleTypes,
            name="schedule_type_enum",
            create_type=True
        ),
        nullable=False
    )
    
    user_id: Mapped[BigInteger] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="schedules"
    )
    
    items: Mapped[List["ScheduleItemsModel"]] = relationship(
        "ScheduleItemsModel",
        back_populates="schedule",
        cascade="all, delete-orphan"
    )
    
    
    def is_item_active_on_date(
        self,
        item: "ScheduleItems",
        day: date,
    ) -> bool:
        if self.type_schedule == ScheduleTypes.DAILY:
            return True
        
        if self.type_schedule == ScheduleTypes.WEEKLY:
            if item.day_of_week is None:
                return False
            
            weekday_map = {
                0: DayOfWeek.MONDAY,
                1: DayOfWeek.TUESDAY,
                2: DayOfWeek.WEDNESDAY,
                3: DayOfWeek.THURSDAY,
                4: DayOfWeek.FRIDAY,
                5: DayOfWeek.SATURDAY,
                6: DayOfWeek.SUNDAY,
            }
            
            return weekday_map[day.weekday()] == item.day_of_week
        return False