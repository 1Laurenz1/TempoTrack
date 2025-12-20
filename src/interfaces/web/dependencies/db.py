from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.session import get_session
from src.infrastructure.database.repositories.user_repository_impl import (
    UserRepositoryImpl   
)


async def get_user_repository(
    session: AsyncSession = Depends(UserRepositoryImpl)
):
    return UserRepositoryImpl(session)