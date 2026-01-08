from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


from src.domain.repositories.schedule_notifications_repository import (
    ScheduleNotificationRepository
)
from src.domain.entities.schedule_notification import ScheduleNotification

from src.common.logging.logger_main import logger

from typing import Optional

from src.infrastructure.database.models.schedule_notification import (
    ScheduleNotificationModel
)
from src.infrastructure.database.mappers.schedule_notification_mapper import (
    ScheduleNotificationMapper
)
from src.infrastructure.exceptions.infrastructure_error import InfrastructureError


class ScheduleNotificationRepositoryImpl(ScheduleNotificationRepository):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
    
    
    async def add(
        self,
        notification: ScheduleNotification
    ) -> Optional[ScheduleNotification]:
        try:
            notification_model = ScheduleNotificationMapper.to_orm(notification)
            
            self.session.add(notification_model)
            await self.session.commit()
            await self.session.refresh(notification_model)
            
            logger.info(f"Notification {notification_model} was successfully created")
            
            return ScheduleNotificationMapper.to_domain(notification_model)
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"An unknown error occurred in add with schedule_notification {notification}")
            raise InfrastructureError("Error reading from the database") from e