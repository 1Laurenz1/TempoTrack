from typing import List
from sqlalchemy import (
    Integer,
    String,
    BigInteger,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM, TIME
from sqlalchemy.ext.hybrid import hybrid_property

from src.infrastructure.database.session import Base
from src.infrastructure.database.mixins.time_stamp_mixin import TimeStampMixin

from src.domain.entities.schedule_items import ScheduleItems

from src.domain.value_objects.day_of_week import DayOfWeek

from datetime import datetime, time


class ScheduleItemsModel(Base, TimeStampMixin):
    __tablename__ = 'schedule_items'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    schedule_id: Mapped[BigInteger] = mapped_column(
        ForeignKey("schedules.id"),
        nullable=False,
        index=True
    )
    
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )
    
    day_of_week: Mapped[DayOfWeek] = mapped_column(
        ENUM(
            DayOfWeek,
            name="day_for_item_enum",
            create_type=True
        ),
        nullable=True,
        default=None
    )
    
    time_start: Mapped[time] = mapped_column(
        TIME(timezone=False),
        nullable=False
    )
    time_end: Mapped[time] = mapped_column(
        TIME(timezone=False),
        nullable=False
    )
    
    user_id: Mapped[BigInteger] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    schedule: Mapped["ScheduleModel"] = relationship(
        "ScheduleModel",
        back_populates="items"
    )
    
    user = relationship("UserModel", back_populates="items")
    
    notifications: Mapped[List["ScheduleNotificationModel"]] = relationship(
        "ScheduleNotificationModel",
        back_populates="schedule_item",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    
    
    @hybrid_property
    def duration(self) -> bool:
        return datetime.combine(datetime.min, self.time_end) - datetime.combine(datetime.min, self.time_start)