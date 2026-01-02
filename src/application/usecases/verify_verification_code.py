from src.application.exceptions.verify import (
    InvalidVerificationCode,
    VerificationCodeNotFound
)

from src.application.ports.verification_code_storage import VerificationCodeStorage

from src.common.utils.verify_code import verify_verification_code


class VerifyVerificationCodeUseCase:
    def __init__(
        self,
        storage: VerificationCodeStorage
    ):
        self.storage = storage
        
        
    async def execute(
        self,
        entered_code: str,
        user_id: int,
    ) -> bool:
        stored_key = await self.storage.get_verify_code_by_user_id(user_id)
        
        if len(entered_code) != 6:
            raise InvalidVerificationCode(
                "The code is not 6 characters long. Please enter the correct code."
            )
        
        if not stored_key:
            raise VerificationCodeNotFound(
                "Verification code not found. The code may have expired"
            )
            
        is_valid = verify_verification_code(stored_key, entered_code)
        
        if is_valid:
            await self.storage.delete_code(user_id)
            return True
        raise InvalidVerificationCode("Invalid verification code")