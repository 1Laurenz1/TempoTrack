from typing import List
from src.application.exceptions.permissions import AccessDeniedError
from src.application.exceptions.schedule import ScheduleNotFoundError
from src.domain.entities.schedule_items import ScheduleItems

from src.application.services.jwt_service import JwtService
from src.application.dto.schedule import (
    AddScheduleItemRequest,
    AddScheduleItemResponse
)

from src.application.exceptions.auth import (
    UserIdNotFoundError,
    UserNotFoundError,
)

from src.domain.repositories.schedule_repository import ScheduleRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.repositories.schedule_items import ScheduleItemsRepository


class AddScheduleItemUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        schedule_items_repository: ScheduleItemsRepository,
        schedule_repository: ScheduleRepository,
    ):
        self.user_repository = user_repository
        self.schedule_items_repository = schedule_items_repository
        self.schedule_repository = schedule_repository
        
    
    async def execute(
        self,
        data: List[AddScheduleItemRequest],
        schedule_id: int,
        user_id: int
    ) -> List[AddScheduleItemResponse]:
        user = await self.user_repository.get_user_by_id(user_id)
        
        if not user:
            return UserNotFoundError(f"User with id={user_id} not found")

        user_schedule = await self.schedule_repository.get_schedule_by_id(schedule_id)

        if not user_schedule:
            raise ScheduleNotFoundError(f"Schedule with id={schedule_id} not found")

        if user_schedule.user_id != user_id:
            raise AccessDeniedError("You do not have access to this schedule")

        if not data:
            return []
        
        domain_items: list[ScheduleItems] = []
        
        for item in data:
            if item.time_start >= item.time_end:
                raise ValueError("time_start must be before time_end")
            
            domain_items.append(
                ScheduleItems(
                    schedule_id=schedule_id,
                    user_id=user_id,
                    name=item.name,
                    description=item.description,
                    time_start=item.time_start,
                    time_end=item.time_end,
                    day_of_week=item.day_of_week,
                )
            )
            
        created_items = await self.schedule_items_repository.add(domain_items, user_id)
        
        return [
            AddScheduleItemResponse(
                name=item.name,
                time_start=item.time_start,
                time_end=item.time_end,
                description=item.description,
                day_of_week=item.day_of_week,
            )
            for item in created_items
        ]