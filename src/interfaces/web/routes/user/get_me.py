from fastapi import APIRouter, HTTPException, Depends, status

from src.application.exceptions.auth import UserNotFoundError
from src.application.exceptions.permissions import AccessDeniedError
from src.application.exceptions.schedule import ScheduleNotFoundError
from src.application.exceptions.validation import InvalidInputError
from src.application.usecases.get_me_usecase import GetMeUseCase

from src.interfaces.web.dependencies.auth import get_current_user_id
from src.interfaces.web.dependencies.usecases import get_users_me_usecase


router = APIRouter()


@router.post(
    "/users/@me",
    status_code=status.HTTP_200_OK
)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    get_me_usecase: GetMeUseCase = Depends(get_users_me_usecase)
):
    try:
        return await get_me_usecase.execute(user_id)
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ScheduleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))