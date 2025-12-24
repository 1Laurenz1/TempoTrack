from fastapi import APIRouter, HTTPException, Depends, Response, status

from src.interfaces.web.schemas.schedules_create import (
    ScheduleCreateRequest,
    ScheduleCreateResponse,
)
from src.interfaces.web.dependencies.usecases import get_create_schedule_usecase
from src.interfaces.web.dependencies.auth import get_current_user_id

from src.application.exceptions.auth import UserNotFoundError

from src.application.usecases.create_schedule import CreateScheduleUseCase


router = APIRouter()


@router.post(
    "/schedules/create/",
    response_model=ScheduleCreateResponse,
    status_code=status.HTTP_200_OK
)
async def create_schedule(
    data: ScheduleCreateRequest,
    user_id: int = Depends(get_current_user_id),
    create_schedule_usecase: CreateScheduleUseCase = Depends(get_create_schedule_usecase),
):
    try:
        result = await create_schedule_usecase.execute(
            user_id=user_id,
            data=data,
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return ScheduleCreateResponse(
        id=result.id,
        name=result.name,
        description=result.description,
        type_schedule=result.type_schedule,
    )