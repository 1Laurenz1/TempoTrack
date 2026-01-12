from enum import Enum


class ScheduleNotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    CANCELED = "canceled"