from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.domain.repositories.schedule_repository import ScheduleRepository
from src.domain.entities.schedule import Schedule

from src.infrastructure.database.models.schedule import ScheduleModel
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.exceptions.infrastructure_error import (
    InfrastructureError
)
from src.infrastructure.database.mappers.schedule_mapper import ScheduleMapper

from src.common.logging.logger_main import logger


from typing import List, Optional


class ScheduleRepositoryImpl(ScheduleRepository):
    def  __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        
        
    async def create(self, schedule: Schedule) -> Optional[Schedule]:
        try:
            schedule_model = ScheduleMapper.to_orm(schedule)
            
            self.session.add(schedule_model)
            await self.session.commit()
            await self.session.refresh(schedule_model)
            
            logger.info(f"Schedule {schedule_model}  was successfully created")
            
            return ScheduleMapper.to_domain(schedule_model)
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error: {e}")
            raise InfrastructureError("Error reading from the database") from e
        
        
    async def get_schedule_by_id(self, id: int) -> Optional[Schedule]:
        try:
            result = await self.session.execute(
                select(ScheduleModel).
                where(ScheduleModel.id == id)
            )
            
            schedule_model = result.scalar_one_or_none()
            
            if schedule_model:
                logger.info(f"Schedule by id {id} was found in the database!")
                return ScheduleMapper.to_domain(schedule_model)
            return None
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise InfrastructureError("Error reading from the database") from e
        
        
    async def get_user_schedules(self, user_id: int) -> List[int]:
        try:
            result = await self.session.execute(
                select(func.count(ScheduleModel.id))
                .select_from(ScheduleModel)
                .where(ScheduleModel.user_id == user_id)
            )
            
            schedules = result.scalars().all()
            
            if not schedules:
                return None
            return schedules
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise InfrastructureError("Error reading from the database") from e
        
        
    async def get_all_user_schedules(self, user_id: int) -> List[Schedule]:
        try:
            result = await self.session.execute(
                select(ScheduleModel)
                .where(ScheduleModel.user_id == user_id)
            )
            
            schedules_orm = result.scalars().all()

            if not schedules_orm:
                return []
            
            schedules = [
                ScheduleMapper.to_domain(schedule)
                for schedule in schedules_orm
            ]
            
            logger.info(f"got {len(schedules)} schedules of user_id: {user_id}")
            
            return schedules
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise InfrastructureError("Error reading from the database") from e
        

    async def get_user_main_schedule(self, user_id: int) -> Optional[Schedule]:
        try:
            result = await self.session.execute(
                select(ScheduleModel)
                .join(UserModel, UserModel.main_schedule == ScheduleModel.id)
                .where(UserModel.id == user_id)
            )

            schedule = result.scalar_one_or_none()
            
            if schedule is None:
                return None
            return schedule
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise InfrastructureError("Error reading from the database") from e
        
        
    async def get_all_users_with_main_schedule(self) -> List[int]:
        try:
            result = await self.session.execute(
                select(UserModel.id)
                .where(~UserModel.main_schedule.is_(None))
            )
            
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise InfrastructureError(
                "Error reading from the database in get_all_users_with_main_schedule"    
            ) from e