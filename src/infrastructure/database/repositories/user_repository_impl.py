from sqlalchemy import select
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

from src.common.logging.logger_main import logger

from pydantic import EmailStr

from typing import Optional


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        try:
            result = self.session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            user_email = result.scalar_one_or_none()
            
            if user_email:
                logger.info(f"User with user email '{user_email}' was found in the database")
                # TODO: Create from_domain and to_domain methods
                ...
            return None
            
        except SQLAlchemyError as e:
            logger.info(f"An unknown error occurred in get_user_by_id: {e}")
            raise InfrastructureError("Error reading from the database") from e
        
        
    async def add(self, user: User) -> Optional[User]:
        try:
            user_model = ... # TODO: Create from_domain and to_domain methods
            
            self.session.add(user_model)
            await self.session.commit()
            self.session.refresh(user_model)
            
            logger.info(f"User {user_model} was successfully created")
            
            return ... # TODO: Create from_domain and to_domain methods 
        except IntegrityError:
            await self.session.rollback()
            logger.error(f"User with email '{user.email}' already exists.")
            raise UserAlreadyExistsError(
                f"User with email '{user.email}' already exists"
            ) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"An unknown error occurred in add with user {user}")
            raise InfrastructureError("Database error") from e