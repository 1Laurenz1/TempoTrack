from dataclasses import dataclass, field
from datetime import datetime, time, timezone

from src.domain.value_objects.notification_status import NotificationStatus


@dataclass
class ScheduledNotification:
    user_id: int
    time_start: time
    time_end: time
    status: NotificationStatus

    payload: str = field(default_factory=str)

    id: int | None = None
    schedule_item_id: int | None = None

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_sent(self) -> None:
        if self.status != NotificationStatus.PENDING:
            raise ValueError("Only pending notifications can be sent")

        self.status = NotificationStatus.SENT

    def mark_failed(self) -> None:
        if self.status != NotificationStatus.PENDING:
            raise ValueError("Only pending notifications can fail")

        self.status = NotificationStatus.FAILED

    def mark_canceled(self) -> None:
        if self.status == NotificationStatus.SENT:
            raise ValueError("Sent notification cannot be canceled")

        self.status = NotificationStatus.CANCELED