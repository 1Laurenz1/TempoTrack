from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.application.exceptions.auth import InvalidUsernameOrEmailOrPasswordError
from src.interfaces.web.schemas.login import (
    LoginUserRequest,
    LoginUserResponse
)
from src.interfaces.web.dependencies.usecases import (
    get_login_usecase
)

from src.infrastructure.exceptions.user_already_exists_error import (
    UserAlreadyExistsError
)
from src.infrastructure.exceptions.infrastructure_error import (
    InfrastructureError
)

from src.application.usecases.login_user import LoginUserUseCase


router = APIRouter()


@router.post(
    "/auth/login/",
    response_model=LoginUserResponse,
    status_code=status.HTTP_200_OK
)
async def login(
    data: LoginUserRequest,
    response: Response,
    login_usecase: LoginUserUseCase = Depends(get_login_usecase),
):
    try:
        login_user = await login_usecase.execute(data)
    except InvalidUsernameOrEmailOrPasswordError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username, email or password"
        )
    except InfrastructureError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

    expires = datetime.now(timezone.utc) + timedelta(days=30)
    response.set_cookie(
        key="refresh_token",
        value=login_user.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
        expires=expires
    )

    return LoginUserResponse(
        access_token=login_user.access_token,
        token_type="bearer",
        username=login_user.username,
        email=login_user.email
    )