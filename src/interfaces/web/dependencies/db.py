from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.session import get_session
from src.infrastructure.database.repositories.user_repository_impl import (
    UserRepositoryImpl   
)
from src.infrastructure.database.repositories.refresh_token_reposiotry_impl import (
    RefreshTokenRepositoryImpl
)
from src.infrastructure.database.repositories.schedule_repository_impl import (
    ScheduleRepositoryImpl
)


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)


def get_refresh_token_repository(
    session: AsyncSession = Depends(get_session),
) -> RefreshTokenRepositoryImpl:
    return RefreshTokenRepositoryImpl(session)


def get_schedule_repository(
    session: AsyncSession = Depends(get_session),
) -> ScheduleRepositoryImpl:
    return ScheduleRepositoryImpl(session)