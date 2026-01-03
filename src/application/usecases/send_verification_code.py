from src.application.ports.telegram_sender import TelegramSender
from src.application.ports.verification_code_storage import VerificationCodeStorage

from src.common.utils.get_verification_code import generate_verification_code


class SendVerificationCodeUseCase:
    def __init__(
        self,
        sender: TelegramSender,
        storage: VerificationCodeStorage,
    ):
        self.sender = sender
        self.storage = storage
        
        
    async def execute(self, username: str, user_id: int):
        code = generate_verification_code()
        
        await self.storage.set_verification_code(
            user_id=user_id,
            code=code
        )
        
        await self.sender.send_verififaction_code(
            user_id=user_id,
            username=username,
            code=code
        )