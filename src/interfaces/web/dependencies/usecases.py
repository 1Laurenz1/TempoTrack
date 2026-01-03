from fastapi import Depends

from src.application.usecases.get_my_schedules import GetMySchedulesUseCase
from src.application.usecases.register_user import RegisterUserUseCase
from src.application.usecases.login_user import LoginUserUseCase
from src.application.usecases.create_schedule import CreateScheduleUseCase
from src.application.usecases.set_main_schedule import SetMainScheduleUseCase
from src.application.usecases.add_item_schedule import AddScheduleItemUseCase
from src.application.usecases.get_me_usecase import GetMeUseCase
from src.application.usecases.send_verification_code import (
    SendVerificationCodeUseCase
)
from src.application.usecases.verify_verification_code import (
    VerifyVerificationCodeUseCase
)
from src.application.usecases.link_telegram_account_database import (
    LinkTelegramAccountDatabaseUseCase
)

from src.infrastructure.redis.verification_code_storage import RedisVerificationCodeStorage

from src.interfaces.bot.ports.telegram_sender_impl import TelegramSenderImpl

from .db import (
    get_user_repository,
    get_refresh_token_repository,
    get_schedule_repository,
    get_schedule_items_repository,
)
from .services import (
    get_password_service,
    get_refresh_token_service,
    get_jwt_service,
)
from .verify import (
    get_telegram_sender_impl,
)
from .redis import (
    get_redis_verification_code_storage,
    get_redis_telegram_indetify_storage
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
    

async def get_set_main_schedule_usecase(
    user_repository = Depends(get_user_repository),
    schedule_repository = Depends(get_schedule_repository),
):
    return SetMainScheduleUseCase(
        user_repository=user_repository,
        schedule_repository=schedule_repository,
    )
    
    
async def get_add_item_schedule_item_usecase(
    user_repository = Depends(get_user_repository),
    schedule_items_repository = Depends(get_schedule_items_repository),
    schedule_repository = Depends(get_schedule_repository),
):
    return AddScheduleItemUseCase(
        user_repository=user_repository,
        schedule_items_repository=schedule_items_repository,
        schedule_repository=schedule_repository,
    )
    
    
async def get_users_me_usecase(
    user_repository = Depends(get_user_repository)
):
    return GetMeUseCase(
        user_repository=user_repository
    )
    

async def get_my_schedules_usecase(
    user_repository = Depends(get_user_repository),
    schedule_repository = Depends(get_schedule_repository),
):
    return GetMySchedulesUseCase(
        user_repository=user_repository,
        schedule_repository=schedule_repository,
    )



async def get_send_verification_code_usecase(
    telegram_sender: TelegramSenderImpl = Depends(get_telegram_sender_impl),
    redis_verification_storage: RedisVerificationCodeStorage = Depends(
        get_redis_verification_code_storage    
    ),
) -> SendVerificationCodeUseCase:
    return SendVerificationCodeUseCase(
        sender=telegram_sender,
        storage=redis_verification_storage,
    )
    
    
async def get_verify_verification_code_usecase(
    redis_verification_storage: RedisVerificationCodeStorage = Depends(
        get_redis_verification_code_storage    
    ),
) -> VerifyVerificationCodeUseCase:
    return VerifyVerificationCodeUseCase(
        storage=redis_verification_storage,
    )
    
    
async def get_link_user_account_database_usecase(
    user_repository = Depends(get_user_repository),
    storage = Depends(get_redis_telegram_indetify_storage),
    sender = Depends(get_telegram_sender_impl)
) -> LinkTelegramAccountDatabaseUseCase:
    return LinkTelegramAccountDatabaseUseCase(
        user_repository=user_repository,
        storage=storage,
        sender=sender
    )