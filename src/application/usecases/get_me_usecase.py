from src.application.dto.user import (
    UserMeResponse
)
from src.application.exceptions.auth import UserNotFoundError

from src.domain.repositories.user_repository import UserRepository



class GetMeUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository
        
        
    async def execute(
        self,
        user_id: int
    ) -> UserMeResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        
        if not user:
            return UserNotFoundError("User not found")
        
        return UserMeResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            tg_username=user.tg_username or "",
            created_at=user.created_at
        )