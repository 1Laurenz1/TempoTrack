from src.application.dto.user import (
    UserMeSchedulesResponse
)

from src.domain.repositories.user_repository import UserRepository
from src.domain.repositories.schedule_repository import ScheduleRepository

from typing import List


class GetMySchedulesUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        schedule_repository: ScheduleRepository,
    ):
        self.user_repository = user_repository
        self.schedule_repository = schedule_repository
        
        
    async def execute(
        self,
        user_id: int
    ) -> List[UserMeSchedulesResponse]:
        schedules = await self.schedule_repository.get_all_user_schedules(user_id)
        
        return [
            UserMeSchedulesResponse(
                id=schedule.id,
                name=schedule.name,
                description=schedule.description or "",
                type_schedule=schedule.type_schedule,
                created_at=schedule.created_at,
                updated_at=schedule.updated_at
            )
            for schedule in schedules
        ]