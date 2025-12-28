from fastapi import APIRouter, HTTPException, status, Depends

from src.application.exceptions.auth import UserNotFoundError
from src.application.exceptions.permissions import AccessDeniedError
from src.application.exceptions.schedule import ScheduleNotFoundError
from src.application.exceptions.validation import InvalidInputError
from src.interfaces.web.dependencies.auth import get_current_user_id
from src.interfaces.web.dependencies.usecases import get_add_item_schedule_item_usecase

from src.interfaces.web.schemas.add_schedule_items import (
    AddScheduleItemRequest,
    AddScheduleItemResponse
)

from src.application.usecases.add_item_schedule import (
    AddScheduleItemUseCase
)


router = APIRouter()


@router.post(
    "/schedules/{schedule_id}/items",
    response_model=list[AddScheduleItemResponse],
    status_code=status.HTTP_201_CREATED,
)
async def add_schedule_items(
    schedule_id: int,
    data: list[AddScheduleItemRequest],
    user_id: int = Depends(get_current_user_id),
    usecase: AddScheduleItemUseCase = Depends(get_add_item_schedule_item_usecase),
):
    try:
        return await usecase.execute(
            user_id=user_id,
            schedule_id=schedule_id,
            data=data,
        )
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ScheduleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))