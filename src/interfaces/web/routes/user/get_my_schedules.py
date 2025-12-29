from fastapi import APIRouter, HTTPException, Depends, status

from src.application.usecases.get_my_schedules import GetMySchedulesUseCase

from src.interfaces.web.dependencies.auth import get_current_user_id
from src.interfaces.web.dependencies.usecases import get_my_schedules_usecase


router = APIRouter()


@router.get(
    "/users/@me/schedules",
    status_code=status.HTTP_200_OK
)
async def get_my_schedules(
    user_id: int = Depends(get_current_user_id),
    get_my_schedules_usecase: GetMySchedulesUseCase = Depends(get_my_schedules_usecase)
):
    return await get_my_schedules_usecase.execute(user_id)