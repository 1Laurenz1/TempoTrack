from fastapi import Depends

from src.application.usecases.register_user import RegisterUserUseCase
from src.application.usecases.login_user import LoginUserUseCase
from src.application.usecases.create_schedule import CreateScheduleUseCase

from .db import (
    get_user_repository,
    get_refresh_token_repository,
    get_schedule_repository,
)
from .services import (
    get_password_service,
    get_refresh_token_service,
    get_jwt_service,
)


async def get_register_user_usecase(
    user_repo = Depends(get_user_repository),
    password_service = Depends(get_password_service)
):
    return RegisterUserUseCase(
        user_repository=user_repo,
        password_service=password_service
    )
    
    
async def get_login_usecase(
    user_repo = Depends(get_user_repository),
    refresh_token_repo = Depends(get_refresh_token_repository),
    refresh_token_service = Depends(get_refresh_token_service),
    jwt_service = Depends(get_jwt_service),
    password_service = Depends(get_password_service),
):
    return LoginUserUseCase(
        user_repository=user_repo,
        refresh_token_repository=refresh_token_repo,
        refresh_token_service=refresh_token_service,
        jwt_service=jwt_service,
        password_service=password_service
    )
    
    
async def get_create_schedule_usecase(
    user_repository = Depends(get_user_repository),
    schedule_repository = Depends(get_schedule_repository),
):
    return CreateScheduleUseCase(
        user_repository=user_repository,
        schedule_repository=schedule_repository,
    )