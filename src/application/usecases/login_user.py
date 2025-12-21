from src.application.services.password_service import PasswordService
from src.domain.entities.refresh_token import RefreshToken  
from src.domain.repositories.refresh_token import RefreshTokenRepository

from src.application.services.refresh_token_service import (
    RefreshTokenService
)
from src.application.services.jwt_service import JwtService
from src.application.dto.login import (
    LoginUserRequest,
    LoginUserResponse
)
from src.application.exceptions.auth import (
    UserNotFoundError,
    InvalidUsernameOrEmailOrPasswordError,
)

from src.domain.repositories.user_repository import UserRepository


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        refresh_token_service: RefreshTokenService,
        jwt_service: JwtService,
        password_service: PasswordService,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.refresh_token_service = refresh_token_service
        self.jwt_service = jwt_service
        self.password_service = password_service
        
        
    async def execute(self, data: LoginUserRequest) -> LoginUserResponse:
            user = await self.user_repository.get_user_by_login(
                data.email or data.username
            )

            if not user:
                raise UserNotFoundError("First, you need to register")

            if not self.password_service.verify(
                data.password,
                user.password
            ):
                raise InvalidUsernameOrEmailOrPasswordError(
                    "Invalid username, email or password"
                )

            raw_refresh_token = self.refresh_token_service.generate()

            refresh_token = RefreshToken(
                user_id=user.id,
                token_hash=self.refresh_token_service.hash(raw_refresh_token),
                expires_at=self.refresh_token_service.get_expiration()
            )

            await self.refresh_token_repository.add(refresh_token)

            access_token = self.jwt_service.create_access_token(
                payload={"sub": str(user.id)}
            )

            return LoginUserResponse(
                email=user.email,
                username=user.username
            )