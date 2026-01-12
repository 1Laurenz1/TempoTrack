from src.infrastructure.database.session import AsyncSessionLocal
from src.infrastructure.database.repositories.schedule_notification import (
    ScheduleNotificationRepositoryImpl
)
from src.infrastructure.database.repositories.user_repository_impl import (
    UserRepositoryImpl
)
from src.infrastructure.redis.redis_client import get_redis_connection

from src.application.usecases.prepare_schedule_notification import (
    PrepareScheduleNotificationUseCase
)

from src.interfaces.bot.ports.telegram_sender_impl import TelegramSenderImpl

from src.domain.value_objects.notification_status import ScheduleNotificationStatus

from src.common.logging.logger_main import logger

from src.infrastructure.celery.app import celery_app

import asyncio


async def send_schedule_notification_task(notification_id: int):
    async with AsyncSessionLocal() as session:
        notification_repo = ScheduleNotificationRepositoryImpl(session)
        user_repo = UserRepositoryImpl(session)

        prepare_usecase = PrepareScheduleNotificationUseCase(notification_repo)

        redis = await get_redis_connection()
        telegram_sender = TelegramSenderImpl()
        

        notification = await notification_repo.get_by_id(notification_id)
        
        username = await user_repo.get_user_tg_username(notification.user_id)
        

        if not notification:
            logger.warning(f"Notification {notification_id} not found")
            return

        if notification.status != ScheduleNotificationStatus.PENDING:
            logger.warning(
                f"Notification {notification.id} skipped, status={notification.status}"
            )
            return

        delay = await prepare_usecase.execute(notification_id)

        if delay is None:
            logger.warning(f"Notification {notification.id} prepare returned None")
            return

        logger.info(
            f"Notification {notification.id} scheduled in {delay:.2f} seconds"
        )

        if delay > 0:
            await asyncio.sleep(delay)
        
        try:
            await telegram_sender.send_notification_message(
                user_id=notification.user_id,
                username=username,
                notification=notification,
            )

            notification.mark_sent()
            
            await notification_repo.delete(notification.id)
            logger.info(f"Notification {notification.id} successfully sent")
        except Exception as e:
            logger.error(f"Failed to send notification {notification_id}: {e}")
            return None
        
        
@celery_app.task(name="tasks.send_schedule_notification")
def send_schedule_notification(notification_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_schedule_notification_task(notification_id))