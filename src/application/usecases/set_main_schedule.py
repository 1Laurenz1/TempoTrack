from src.domain.entities.schedule import Schedule
from src.domain.repositories.schedule_repository import ScheduleRepository
from src.domain.repositories.user_repository import UserRepository

from src.application.exceptions.auth import UserNotFoundError
from src.application.exceptions.validation import InvalidInputError
from src.application.exceptions.permissions import AccessDeniedError
from src.application.exceptions.schedule import ScheduleNotFoundError

from src.application.dto.schedule import (
    SetMainScheduleRequest,
    SetMainScheduleResponse
)


class SetMainScheduleUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        schedule_repository: ScheduleRepository,
    ):
        self.user_repository = user_repository
        self.schedule_repository = schedule_repository
        
    
    async def execute(
        self,
        data: SetMainScheduleRequest,
        user_id: int,
    ) -> SetMainScheduleResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        
        if not user:
            raise UserNotFoundError("User not found. Please try logging in or registering.")
        
        if not data.schedule_id:
            raise InvalidInputError("schedule_id is required")
        
        user_schedule = await self.schedule_repository.get_schedule_by_id(data.schedule_id)

        if not user_schedule:
            raise ScheduleNotFoundError("Schedule not found")
        
        if user_schedule.user_id != user_id:
            raise AccessDeniedError("You do not have access to this schedule")
        
        await self.user_repository.set_main_schedule(
            user_id=user_id,
            schedule_id=data.schedule_id
        )
        
        return SetMainScheduleResponse(
            schedule_id=data.schedule_id,
            schedule_name=user_schedule.name
        )