from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.domain.repositories.schedule_notifications_repository import (
    ScheduleNotificationRepository
)
from src.domain.entities.schedule_notification import ScheduleNotification
from src.domain.value_objects.notification_status import (
    ScheduleNotificationStatus
)

from src.common.logging.logger_main import logger

from src.infrastructure.database.models.schedule_notification import (
    ScheduleNotificationModel
)
from src.infrastructure.database.mappers.schedule_notification_mapper import (
    ScheduleNotificationMapper
)
from src.infrastructure.exceptions.infrastructure_error import InfrastructureError

from typing import Optional, List


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
            raise InfrastructureError("Database error while creating notification") from e
        
        
    async def add_many(
        self,
        notifications: List[ScheduleNotification],
    ) -> List[ScheduleNotification]:
        try:
            notifications_model = [
                ScheduleNotificationMapper.to_orm(notification)
                for notification in notifications
            ]
            
            self.session.add_all(notifications_model)
            await self.session.commit()
            
            for model in notifications_model:
                await self.session.refresh(model)
            
            logger.info(f"Notifications {notifications_model}")
            
            return [
                ScheduleNotificationMapper.to_domain(notification)
                for notification in notifications_model
            ]
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                f"Error while creating schedule_notifications: {notifications}",
                exc_info=True,
            )
            raise InfrastructureError("Database error while creating notifications") from e
        
    
    async def get_by_user_id(
        self,
        user_id: int,
    ) -> List[ScheduleNotification]:
        result = await self.session.execute(
            select(ScheduleNotificationModel)
            .where(ScheduleNotificationModel.user_id == user_id)
        )
        orm_notifications = result.scalars().all()
        return [ScheduleNotificationMapper.to_domain(n) for n in orm_notifications]
    
    
    async def get_by_id(
        self,
        notification_id: int,
    ) -> Optional[ScheduleNotification]:
        try:
            result = await self.session.execute(
                select(ScheduleNotificationModel)
                .where(ScheduleNotificationModel.id == notification_id)
            )
            
            orm_notification = result.scalar_one_or_none()
            
            if orm_notification is None:
                return None
            return ScheduleNotificationMapper.to_domain(orm_notification)
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                f"Error while retrieving notifications with notification_id: {notification_id}",
                exc_info=True,
            )
            raise InfrastructureError(
                f"Database error while retrieving notifications with notification_id: {notification_id}"    
            ) from e
            
    
    async def delete(
        self,
        notification_id: int,
    ) -> Optional[ScheduleNotification]:
        try:
            orm_notification = await self.session.get(
                ScheduleNotificationModel, notification_id
            )
            
            if not orm_notification:
                return None
            
            deleted_notification = orm_notification
            
            await self.session.delete(deleted_notification)
            await self.session.commit()
            
            logger.info(
                f"Notification {orm_notification}({orm_notification.id}) was deleted successfully"
            )
            return ScheduleNotificationMapper.to_domain(orm_notification)
            
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                f"Error deleting notification {notification_id}",
                exc_info=True
            )
            raise InfrastructureError(
                f"Database error deleting notification {notification_id}"
            ) from e