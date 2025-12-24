import pytest
import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.domain.entities.user import User
from src.infrastructure.database.models.refresh_token import RefreshTokenModel
from src.domain.entities.refresh_token import RefreshToken
from src.infrastructure.database.repositories.refresh_token_reposiotry_impl import (
    RefreshTokenRepositoryImpl
)
from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from src.application.services.refresh_token_service import (
    RefreshTokenService
)


@pytest.mark.asyncio
async def test_add_refresh_token_success(db_session: AsyncSession):
    repo = RefreshTokenRepositoryImpl(db_session)
    user_repository = UserRepositoryImpl(db_session)
    refresh_token_service = RefreshTokenService()

    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=1,
        main_schedule=1
    )
    
    await user_repository.add(user)

    token = RefreshToken(
        user_id=1,
        token_hash="test_token_1",
        expires_at=refresh_token_service.get_expiration()
    )
    
    refresh_token_service.hash(token.token_hash)
    
    created = await repo.add(token)
    
    assert created.id is not None
    assert created.user_id == token.user_id
    assert created.token_hash != token.token_hash
    assert created.revoked is False


@pytest.mark.asyncio
async def test_add_refresh_token_retry_on_collision(db_session: AsyncSession):
    repo = RefreshTokenRepositoryImpl(db_session)
    user_repository = UserRepositoryImpl(db_session)
    refresh_token_service = RefreshTokenService()


    token_hash = b"collision_token"

    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=1,
        main_schedule=1
    )
    
    await user_repository.add(user)
    
    token2 = RefreshToken(
        user_id=1,
        token_hash=token_hash,
        expires_at=refresh_token_service.get_expiration()
    )
    created2 = await repo.add(token2)
    
    assert created2.token_hash == token_hash
    assert created2.user_id == token2.user_id


@pytest.mark.asyncio
async def test_get_by_hash_not_found(db_session: AsyncSession):
    repo = RefreshTokenRepositoryImpl(db_session)
    
    result = await repo.get_by_hash(b"nonexistent_token")
    assert result is None