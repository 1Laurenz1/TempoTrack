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

from src.interfaces.web.dependencies.usecases import get_send_verification_code_usecase

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
    response_model=VerifyCodeRequest,
    status_code=status.HTTP_200_OK,
)
async def verify_code(
    data: VerifyCodeResponse,
    user_id: int = Depends(get_current_user_id),
    usecase: ... = Depends(...)
):
    """
    Step 2: Verify the code entered by the user on the website.

    The user enters the verification code they received in Telegram. 
    This endpoint checks the code against the stored value in Redis.
        
    ⚠️ Note: This router is not fully finished and should be used carefully.
    """
    is_valid = await usecase.execute(user_id=user_id, code=data.code)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )

    return VerifyCodeRequest(
        message="Verification successful"
    )