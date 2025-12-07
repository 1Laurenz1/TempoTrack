from sqlalchemy import (
    Integer,
    String,
    BigInteger,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM

from src.infrastructure.database.session import Base
from src.infrastructure.database.mixins.time_stamp_mixin import TimeStampMixin

from src.domain.entities.schedule import Schedule

from src.domain.value_objects.schedule_types import ScheduleTypes


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
    
    telegram_id: Mapped[BigInteger] = mapped_column(
        ForeignKey("users.telegram_id"),
        nullable=False,
        index=True
    )