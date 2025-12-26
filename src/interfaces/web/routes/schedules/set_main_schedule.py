from fastapi import APIRouter, HTTPException, Depends, Response, status

from src.application.exceptions.auth import UserNotFoundError
from src.application.exceptions.permissions import AccessDeniedError
from src.application.exceptions.schedule import ScheduleNotFoundError
from src.application.exceptions.validation import InvalidInputError
from src.interfaces.web.schemas.set_main_schedule import (
    SetMainScheduleRequest,
    SetMainScheduleResponse
)
from src.application.usecases.set_main_schedule import (
    SetMainScheduleUseCase
)

from src.interfaces.web.dependencies.auth import get_current_user_id
from src.interfaces.web.dependencies.usecases import get_set_main_schedule_usecase


router = APIRouter()


@router.post(
    "/schedules/set_main_schedule/",
    response_model=SetMainScheduleResponse,
    status_code=status.HTTP_200_OK
)
async def create_schedule(
    data: SetMainScheduleRequest,
    user_id: int = Depends(get_current_user_id),
    set_main_schedule_usecase: SetMainScheduleUseCase = Depends(get_set_main_schedule_usecase),
):
    try:
        result = await set_main_schedule_usecase.execute(
            data=data,
            user_id=user_id
        )
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ScheduleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
        
    return SetMainScheduleResponse(
        schedule_id=int(data.schedule_id),
        schedule_name=result.schedule_name,
    )