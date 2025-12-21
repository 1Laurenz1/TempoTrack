from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.domain.repositories.refresh_token import RefreshTokenRepository
from src.domain.entities.refresh_token import RefreshToken

from src.infrastructure.database.models.refresh_token import RefreshTokenModel
from src.infrastructure.exceptions.infrastructure_error import (
    InfrastructureError
)

from src.common.logging.logger_main import logger

from typing import Optional


class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    
    async def exists_refresh_token(self, token_hash: bytes) -> Optional[RefreshToken]:
        try:
            result = await self.session.execute(
                select(RefreshTokenModel).
                where(RefreshTokenModel.token_hash == token_hash)
            )
            
            refresh_token_model = result.scalar_one_or_none()
            
            if refresh_token_model:
                logger.info(f"Refresh token {token_hash} was found in the database")
                #TODO: Return the domain entity RefreshToken
            return None
        except SQLAlchemyError as e:
            logger.info(f"An unknown error occurred in exists_refresh_token: {e}")
            raise InfrastructureError("Error reading from the database") from e
        
        
    async def add(self, refresh_token: RefreshToken) -> Optional[RefreshToken]:
        try:
            refresh_token_model = ... #TODO: Convert a domain entity to ORM
            
            self.session.add(refresh_token_model)
            await self.session.commit()
            await self.session.refresh(refresh_token_model)
            
            logger.info(f"refresh token {refresh_token} was successfully created")
            
            #TODO: Convert an ORM model into an entity
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Hashed refresh token already exists:\n{refresh_token.token_hash}")
            #TODO: return RefreshTokenAlreadyExistsError
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"An unknown error occurred in add with refresh token {refresh_token}")
            raise InfrastructureError("Database error") from e