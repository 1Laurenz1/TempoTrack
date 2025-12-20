from fastapi import Depends

from src.application.usecases.register_user import RegisterUserUseCase

from .db import get_user_repository
from .password import get_password_service


async def get_register_user_usecase(
    user_repo = Depends(get_user_repository),
    password_service = Depends(get_password_service)
):
    return RegisterUserUseCase(
        user_repository=user_repo,
        password_service=password_service
    )