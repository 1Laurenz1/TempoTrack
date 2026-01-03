from fastapi import APIRouter, Depends, HTTPException, status

from src.interfaces.web.dependencies.auth import get_current_user_id
from src.interfaces.web.schemas.verify import (
    VerificationAccountRequest,
    VerificationAccountResponse,
    VerifyCodeRequest,
    VerifyCodeResponse
)

from src.application.usecases.send_verification_code import (
    SendVerificationCodeUseCase
)
from src.application.usecases.verify_verification_code import (
    VerifyVerificationCodeUseCase
)
from src.application.usecases.link_telegram_account_database import (
    LinkTelegramAccountDatabaseUseCase
)

from src.interfaces.web.dependencies.usecases import get_send_verification_code_usecase
from src.interfaces.web.dependencies.usecases import get_verify_verification_code_usecase
from src.interfaces.web.dependencies.usecases import get_link_user_account_database_usecase


router = APIRouter()


@router.post(
    "/users/@me/verify_account",
    response_model=VerificationAccountResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_account(
    data: VerificationAccountRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: SendVerificationCodeUseCase = Depends(get_send_verification_code_usecase)
):
    """
    Step 1: Send verification code to Telegram user.

    The user provides their Telegram username. 
    A verification code will be sent to this username via the Telegram bot.
    
    ⚠️ IMPORTANT: The user must have already started a chat with the bot. 
    Otherwise, sending the code will fail.
    """
    try:
        await usecase.execute(user_id=user_id, username=data.username)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return VerificationAccountResponse(
        message=f"Verification code sent to Telegram user @{data.username}"
    )


@router.post(
    "/users/@me/verify_code",
    response_model=VerifyCodeResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_code(
    data: VerifyCodeRequest,
    user_id: int = Depends(get_current_user_id),
    verify_code_usecase: VerifyVerificationCodeUseCase = Depends(get_verify_verification_code_usecase),
    set_data_to_database_usecase: LinkTelegramAccountDatabaseUseCase = Depends(
        get_link_user_account_database_usecase
    )
):
    """
    Step 2: Verify the code entered by the user on the website.

    The user enters the verification code they received in Telegram. 
    This endpoint checks the code against the stored value in Redis.
        
    """
    is_valid = await verify_code_usecase.execute(entered_code=data.code, user_id=user_id)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    await set_data_to_database_usecase.execute(
        user_id=user_id,
    )

    return VerifyCodeResponse(
        success=True,
        message="verification successfull"
    )