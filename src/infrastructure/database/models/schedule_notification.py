from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM, TIME

from src.infrastructure.database.session import Base
from src.infrastructure.database.mixins.time_stamp_mixin import TimeStampMixin

from src.domain.value_objects.notification_status import ScheduleNotificationStatus

from datetime import time
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user import UserModel
    from .schedule_items import ScheduleItemsModel


class ScheduleNotificationModel(Base, TimeStampMixin):
    __tablename__ = "schedule_notifications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    
    schedule_item_id: Mapped[int] = mapped_column(
        ForeignKey("schedule_items.id"),
        nullable=False,
        index=True,
    )

    time_start: Mapped[time] = mapped_column(
        TIME,
        nullable=False,
    )

    time_end: Mapped[time] = mapped_column(
        TIME,
        nullable=False,
    )

    payload: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="",
    )

    status: Mapped[ScheduleNotificationStatus] = mapped_column(
        ENUM(
            ScheduleNotificationStatus,
            name="schedule_notification_status_enum",
            create_type=True,
        ),
        nullable=False,
    )

    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="notifications",
    )
    schedule_item: Mapped["ScheduleItemsModel"] = relationship(
        "ScheduleItemsModel",
        back_populates="notifications",
    )