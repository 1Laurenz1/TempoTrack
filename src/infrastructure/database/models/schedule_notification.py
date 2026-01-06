from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM, TIME

from src.infrastructure.database.session import Base
from src.infrastructure.database.mixins.time_stamp_mixin import TimeStampMixin
from src.domain.value_objects.notification_status import ScheduledNotificationStatus
from src.domain.entities.schedule_notification import ScheduledNotification


class ScheduleNotificationModel(Base, TimeStampMixin):
    __tablename__ = 'schedule_notifications'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False,
        index=True
    )
    
    schedule_item_id: Mapped[int] = mapped_column(
        ForeignKey('schedule_items.id'),
        nullable=False,
        index=True
    )

    status: Mapped[ScheduledNotificationStatus] = mapped_column(
        ENUM(
            ScheduledNotificationStatus,
            name="schedule_notification_status_enum",
            create_type=True
        ),
        nullable=True,
        default=None
    )
    
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="notifications")
    schedule_item: Mapped["ScheduleItemModel"] = relationship("ScheduleItemModel", back_populates="notifications")