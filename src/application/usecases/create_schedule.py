from src.application.dto.schedule import (
    ScheduleCreateRequest,
    ScheduleCreateResponse
)
from src.application.exceptions.auth import UserNotFoundError

from src.domain.entities.schedule import Schedule
from src.domain.repositories.user_repository import UserRepository
from src.domain.repositories.schedule_repository import ScheduleRepository



class CreateScheduleUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        schedule_repository: ScheduleRepository,
    ):
        self.user_repository = user_repository
        self.schedule_repository = schedule_repository
        
        
    async def execute(
        self,
        data: ScheduleCreateRequest,
        user_id: int
    ) -> ScheduleCreateResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        schedule = Schedule(
            user_id=user_id,
            name=data.name,
            description=data.description,
            type_schedule=data.type_schedule,
        )

        created = await self.schedule_repository.create(schedule)
        
        await self.user_repository.increment_schedules_count(user_id)

        return ScheduleCreateResponse(
            id=created.id,
            name=created.name,
            description=created.description,
            type_schedule=created.type_schedule,
        )