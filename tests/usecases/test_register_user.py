from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecases.register_user import RegisterUserUseCase

from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl

from src.application.services.password_service import (
    PasswordService
)
from src.application.dto.register import (
    RegisterUserRequest,
    RegisterUserResponse
)

import pytest



@pytest.mark.asyncio
async def test_register_user_usecase(db_session: AsyncSession):
    register_user_usecase = RegisterUserUseCase(
        user_repository=UserRepositoryImpl(db_session),
        password_service=PasswordService()
    )
    
    data = RegisterUserRequest(
        email="John@example.com",
        username="John123",
        password="top_secret",
        first_name="John",
        last_name="Doe"
    )
    
    assert data.password == "top_secret"
    
    result = await register_user_usecase.execute(data)
    
    assert result.email == "John@example.com"
    assert result.username == "John123"
    assert result.first_name == "John"
    assert result.last_name == "Doe"