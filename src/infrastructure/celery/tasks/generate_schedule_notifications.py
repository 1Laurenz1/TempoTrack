import asyncio
from src.infrastructure.database.session import AsyncSessionLocal
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

from src.common.logging.logger_main import logger

from .send_schedule_notification import send_schedule_notification

from src.infrastructure.celery.app import celery_app


async def generate_schedule_notifications_task():
    async with AsyncSessionLocal() as session:
        usecase = GenerateScheduleNotificationsUseCase(
            schedule_repo=ScheduleRepositoryImpl(session),
            schedule_items_repo=ScheduleItemsRepositoryImpl(session),
            schedule_notification_repo=ScheduleNotificationRepositoryImpl(session),
        )

        user_ids = await usecase.schedule_repo.get_all_users_with_main_schedule()
        logger.info(f"Found {len(user_ids)} users with main schedule: {user_ids}")

        for user_id in user_ids:
            try:
                notifications = await usecase.execute(user_id)
                logger.info(f"Notifications generated for user_id={user_id}")
                
                for notification in notifications:
                    send_schedule_notification.delay(notification.id)
            
            except Exception:
                logger.exception(f"Failed to generate notifications for user_id={user_id}")


@celery_app.task(name="tasks.generate_schedule_notifications")
def generate_schedule_notifications():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_schedule_notifications_task())
    # asyncio.run(generate_schedule_notifications_task())