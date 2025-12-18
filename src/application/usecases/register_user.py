from src.infrastructure.database.repositories.user_repository_impl import (
    UserRepositoryImpl
)
from src.application.services.password_service import (
    PasswordService
)



class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: ...,
        password_service: ...,
    ):
        self.user_repository = ...
        self.password_service = ...
        
    
    async def execute(self):
        ...