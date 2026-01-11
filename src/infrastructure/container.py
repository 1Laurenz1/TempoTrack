
from src.infrastructure.database.session import get_session
from src.infrastructure.database.repositories.schedule_repository_impl import (
    ScheduleRepositoryImpl
)
from src.infrastructure.database.repositories.schedule_items_repository_impl import (
    ScheduleItemsRepositoryImpl
)
from src.infrastructure.database.repositories.schedule_notification import (
    ScheduleNotificationRepositoryImpl
)

from src.application.usecases.generate_schedule_notifications import (
    GenerateScheduleNotificationsUseCase
)



async def get_generate_schedule_notifications_usecase():
    async with get_session() as session:
        schedule_repo = ScheduleRepositoryImpl(session)
        schedule_items_repo = ScheduleItemsRepositoryImpl(session)
        schedule_notifications_repo = ScheduleNotificationRepositoryImpl(session)
        
        return GenerateScheduleNotificationsUseCase(
            schedule_items_repo=schedule_items_repo,
            schedule_repo=schedule_repo,
            schedule_notification_repo=schedule_notifications_repo,
        )