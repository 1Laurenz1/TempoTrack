from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository

from src.application.services.password_service import (
    PasswordService
)
from src.application.dto.register import (
    RegisterUserRequest,
    RegisterUserResponse
)



class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        
    
    async def execute(self, data: RegisterUserRequest) -> RegisterUserResponse:
        hashed_password = self.password_service.hash(data.password)
        
        user = User(
            username=data.username,
            email=data.email,
            password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        
        created_user = await self.user_repository.add(user)
        
        return RegisterUserResponse(
            username=created_user.username,
            email=created_user.email,
            first_name=created_user.first_name or "",
            last_name=created_user.last_name or "",
        )