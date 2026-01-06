from enum import Enum


class ScheduledNotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    CANCELED = "canceled"