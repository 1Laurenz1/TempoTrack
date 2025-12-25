from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.domain.repositories.user_repository import UserRepository
from src.domain.entities.user import User

from src.infrastructure.database.models.user import UserModel
from src.infrastructure.exceptions.infrastructure_error import (
    InfrastructureError
)
from src.infrastructure.exceptions.user_already_exists_error import (
    UserAlreadyExistsError
)
from src.infrastructure.exceptions.user_not_found_error import (
    UserNotFoundError
)
from src.infrastructure.database.mappers.user_mapper import UserMapper

from src.common.logging.logger_main import logger

from pydantic import EmailStr

from typing import Optional


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def get_user_by_id(self, id: int) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(UserModel).where(UserModel.id == id)
            )
            user_model = result.scalar_one_or_none()
            
            if user_model:
                logger.info(f"User with user id '{id}' was found in the database")
                return UserMapper.to_domain(user_model)
            return None
            
        except SQLAlchemyError as e:
            logger.info(f"An unknown error occurred in get_user_by_id: {e}")
            raise InfrastructureError("Error reading from the database") from e

        
    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            user_model = result.scalar_one_or_none()
            
            if user_model:
                logger.info(f"User with user email '{email}' was found in the database")
                return UserMapper.to_domain(user_model)
            return None
            
        except SQLAlchemyError as e:
            logger.info(f"An unknown error occurred in get_user_by_email: {e}")
            raise InfrastructureError("Error reading from the database") from e
        
        
    async def get_user_by_login(
        self,
        login: str
    ) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(UserModel).where(
                    or_(
                        UserModel.email == login,
                        UserModel.username == login
                    )
                )
            )

            user_model = result.scalar_one_or_none()

            if user_model:
                logger.info(f"User with login '{login}' was found in the database")
                return UserMapper.to_domain(user_model)
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error in get_user_by_login: {e}")
            raise InfrastructureError("Error reading from the database") from e
        
        
    async def add(self, user: User) -> Optional[User]:
        try:
            user_model = UserMapper.to_orm(user)
            
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
            
            logger.info(f"User {user_model} was successfully created")
            
            return UserMapper.to_domain(user_model)
        except IntegrityError:
            await self.session.rollback()
            logger.error(f"User with email '{user.email}' already exists.")
            raise UserAlreadyExistsError(
                f"User with email '{user.email}' already exists"
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"An unknown error occurred in add with user {user}")
            raise InfrastructureError("Error reading from the database") from e
        
    
    async def increment_schedules_count(self, user_id: int) -> None:
        try:
            result = await self.session.execute(
                update(UserModel)
                .where(UserModel.id == user_id)
                .values(schedules_count=UserModel.schedules_count + 1)
            )
            
            updated_user = result.scalar_one_or_none()
            
            if not updated_user:
                raise UserNotFoundError(f"User with id {user_id} not found")
            
            await self.session.commit()
            
            logger.info(
                f"The number of schedules for the user with user_id {user_id} has been increased by 1"
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                f"An unknown error occurred in increment_schedules_count with user_id {user_id}"
            )
            raise InfrastructureError("Error reading from the database") from e
        
        
    async def decrement_schedules_count(self, user_id: int) -> None:
        try:
            result = await self.session.execute(
                update(UserModel)
                .where(
                    UserModel.id == user_id,
                    UserModel.schedules_count > 0
                )
                .values(schedules_count=UserModel.schedules_count - 1)
            )
            
            updated_user = result.scalar_one_or_none()
            
            if not updated_user:
                raise UserNotFoundError(f"User with id {user_id} not found")

            await self.session.commit()

            logger.info(
                f"The number of schedules for the user with user_id {user_id} has been reduced by 1"
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise InfrastructureError("Database error") from e
        
        
    async def set_main_schedule(
        self,
        user_id: int,
        schedule_id: Optional[int],
    ) -> None:
        try:
            updated_user = await self.session.execute(
                update(UserModel)
                .where(UserModel.id == user_id)
                .values(main_schedule = schedule_id)
            )
            
            updated_user = updated_user.scalar_one_or_none()
            
            if not updated_user:
                raise UserNotFoundError(f"User with id {user_id} not found")
            await self.session.commit()
            logger.info(f"Set main_schedule={schedule_id} for user {user_id}")
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise InfrastructureError("Database error") from e