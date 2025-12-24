from src.application.dto.schedule import (
    ScheduleCreateRequest,
    ScheduleCreateResponse
)

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
        schedule = await self.schedule_repository.create(data)
        
        return ScheduleCreateResponse(
            id=schedule.id,
            name=schedule.name,
            description=schedule.description or "",
            type_schedule=schedule.type_schedule
        )