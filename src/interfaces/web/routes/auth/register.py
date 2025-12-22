from fastapi import APIRouter, Depends, HTTPException, status

from src.interfaces.web.schemas.register import (
    RegisterUserRequest,
    RegisterUserResponse
)
from src.interfaces.web.dependencies.usecases import get_register_user_usecase

from src.infrastructure.exceptions.user_already_exists_error import (
    UserAlreadyExistsError
)
from src.infrastructure.exceptions.infrastructure_error import (
    InfrastructureError
)

from src.application.usecases.register_user import RegisterUserUseCase


router = APIRouter()


@router.post(
    "/register",
    response_model=RegisterUserResponse,
    status_code=status.HTTP_200_OK
)
async def register(
    data: RegisterUserRequest,
    register_usecase: RegisterUserUseCase = Depends(get_register_user_usecase),
):
    try:
        created_user = await register_usecase.execute(data)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=400, detail="User already exists")
    except InfrastructureError:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return created_user