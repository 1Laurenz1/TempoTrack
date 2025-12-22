from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.application.services.refresh_token_service import RefreshTokenService
from src.domain.repositories.refresh_token import RefreshTokenRepository
from src.domain.entities.refresh_token import RefreshToken

from src.infrastructure.database.models.refresh_token import RefreshTokenModel
from src.infrastructure.database.mappers.refresh_token_mapper import (
    RefreshTokenMapper
)
from src.infrastructure.exceptions.infrastructure_error import (
    InfrastructureError
)

from src.common.logging.logger_main import logger

from typing import Optional


MAX_RETRIES = 5

class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.token_service = RefreshTokenService()

    async def add(self, refresh_token: RefreshToken) -> RefreshToken:
        retries = 0
        while retries < MAX_RETRIES:
            try:
                orm_token = RefreshTokenMapper.to_orm(refresh_token)
                self.session.add(orm_token)
                await self.session.commit()
                await self.session.refresh(orm_token)

                logger.info(f"Refresh token successfully created for user {refresh_token.user_id}")
                return RefreshTokenMapper.to_domain(orm_token)

            except IntegrityError:
                await self.session.rollback()
                retries += 1
                logger.warning(f"Token hash collision detected, retry {retries}/{MAX_RETRIES}")
                refresh_token.token_hash = self.token_service.create_refresh_token()

            except SQLAlchemyError as e:
                await self.session.rollback()
                logger.error(f"Unknown DB error while adding refresh token: {e}")
                raise InfrastructureError("Database error") from e

        raise InfrastructureError("Unable to create unique refresh token after multiple attempts")

    async def get_by_hash(self, token_hash: bytes) -> Optional[RefreshToken]:
        try:
            result = await self.session.execute(
                select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash)
            )
            orm_token = result.scalar_one_or_none()
            if orm_token:
                return RefreshTokenMapper.to_domain(orm_token)
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error fetching refresh token by hash: {e}")
            raise InfrastructureError("Error reading from database") from e