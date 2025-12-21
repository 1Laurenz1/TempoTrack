from sqlalchemy.ext.asyncio import AsyncSession


from src.infrastructure.database.models.refresh_token import (
    RefreshTokenModel
)

from src.domain.entities.refresh_token import RefreshToken

import pytest


@pytest.mark.asyncio
async def test_refresh_session_creation_orm(db_session: AsyncSession):
    ...