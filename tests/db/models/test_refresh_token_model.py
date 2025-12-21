from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.password_service import PasswordService
from src.infrastructure.database.models.refresh_token import (
    RefreshTokenModel
)
from src.infrastructure.database.models.user import (
    UserModel
)

from src.domain.entities.refresh_token import RefreshToken

from src.application.services.refresh_token_service import (
    RefreshTokenService
)

from datetime import datetime, timedelta, timezone

import pytest


@pytest.mark.asyncio
async def test_refresh_session_creation_orm(db_session: AsyncSession):
    refresh_token_manager = RefreshTokenService()
    password_manager = PasswordService()
    
    user = UserModel(
        username="John",
        email="john@example.com",
        password=password_manager.hash("secret"),
        first_name="John",
        last_name="Alderson",
        tg_username="JohnAlderson",
        telegram_id=1846256732,
        schedules_count=3,
        main_schedule=2
    )
    
    db_session.add(user)
    await db_session.commit()
    
    token = refresh_token_manager.create_refresh_token()
    
    refresh_session = RefreshTokenModel(
        user_id=1,
        token_hash=refresh_token_manager.hash(token),
        expires_at=refresh_token_manager.get_expiration()
    )
    
    db_session.add(refresh_session)
    
    await db_session.commit()
    await db_session.refresh(refresh_session)
    
    assert refresh_session.user_id == 1
    assert isinstance(refresh_session.expires_at, datetime)
    assert isinstance(refresh_session.token_hash, bytes)
    assert isinstance(refresh_session.created_at, datetime)
    assert isinstance(refresh_session.updated_at, datetime)
    
    
@pytest.mark.asyncio
async def test_refresh_session_revoked(db_session):
    refresh_token_manager = RefreshTokenService()

    user = UserModel(
        username="John",
        email="john@example.com",
        password=b"secret",
        first_name="John",
        last_name="Alderson",
        tg_username="JohnAlderson",
        telegram_id=1846256732,
        schedules_count=3,
        main_schedule=2
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = refresh_token_manager.create_refresh_token()
    
    refresh_session = RefreshTokenModel(
        user_id=user.id,
        token_hash=refresh_token_manager.hash(token),
        expires_at=refresh_token_manager.get_expiration()
    )
    
    db_session.add(refresh_session)
    await db_session.commit()
    await db_session.refresh(refresh_session)

    refresh_session.revoked = True
    await db_session.commit()
    await db_session.refresh(refresh_session)
    
    assert refresh_session.revoked is True


@pytest.mark.asyncio
async def test_refresh_session_expired(db_session):
    refresh_token_manager = RefreshTokenService()

    user = UserModel(
        username="John",
        email="john@example.com",
        password=b"secret",
        first_name="John",
        last_name="Alderson",
        tg_username="JohnAlderson",
        telegram_id=1846256732,
        schedules_count=3,
        main_schedule=2
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = refresh_token_manager.create_refresh_token()

    refresh_session = RefreshTokenModel(
        user_id=user.id,
        token_hash=refresh_token_manager.hash(token),
        expires_at=refresh_token_manager.get_expiration()
    )
    
    db_session.add(refresh_session)
    await db_session.commit()
    await db_session.refresh(refresh_session)

    assert refresh_session.expires_at > datetime.now(timezone.utc)