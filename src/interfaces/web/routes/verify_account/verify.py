from fastapi import APIRouter, HTTPException, status, Depends

from src.interfaces.web.dependencies.auth import get_current_user_id

from src.interfaces.web.schemas.verify import (
    VerificationAccountRequest,
    VerificationAccountResponse,
    VerifyCodeResponse,
    VerifyCodeRequest
)

from src.application.usecases.send_verification_code import (
    SendVerificationCodeUseCase
)


router = APIRouter()


@router.post(
    "/users/@me/verify_account",
    response_model=VerificationAccountResponse,
    status_code=status.HTTP_200_OK,
)
async def add_schedule_items(
    data: VerificationAccountRequest,
    user_id: int = Depends(get_current_user_id),
):
    ...
    
    
@router.post(
    "/users/@me/verify_code",
    response_model=VerifyCodeRequest,
    status_code=status.HTTP_200_OK,
)
async def add_schedule_items(
    data: VerifyCodeResponse,
    user_id: int = Depends(get_current_user_id),
):
    ...