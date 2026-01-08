from src.domain.entities.schedule_notification import ScheduleNotification
from src.infrastructure.database.models.schedule_notification import (
    ScheduleNotificationModel,
)


class ScheduleNotificationMapper:
    @staticmethod
    def to_domain(model: ScheduleNotificationModel) -> ScheduleNotification:
        return ScheduleNotification(
            id=model.id,
            user_id=model.user_id,
            schedule_item_id=model.schedule_item_id,
            time_start=model.time_start,
            time_end=model.time_end,
            payload=model.payload,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: ScheduleNotification) -> ScheduleNotificationModel:
        return ScheduleNotificationModel(
            id=entity.id,
            user_id=entity.user_id,
            schedule_item_id=entity.schedule_item_id,
            time_start=entity.time_start,
            time_end=entity.time_end,
            payload=entity.payload,
            status=entity.status,
        )
