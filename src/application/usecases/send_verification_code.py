from src.application.ports.telegram_sender import TelegramSender
from src.application.ports.verification_code_storage import VerificationCodeStorage
from src.application.exceptions.schedule import MainScheduleNotSetError

from src.domain.repositories.schedule_repository import ScheduleRepository

from src.common.utils.get_verification_code import generate_verification_code


class SendVerificationCodeUseCase:
    def __init__(
        self,
        sender: TelegramSender,
        storage: VerificationCodeStorage,
        schedule_repo: ScheduleRepository, 
    ):
        self.sender = sender
        self.storage = storage
        self.schedule_repo = schedule_repo
        
        
    async def execute(self, username: str, user_id: int):
        code = generate_verification_code()
        has_main_schedule = await self.schedule_repo.get_user_main_schedule(user_id)
        
        if not has_main_schedule:
            raise MainScheduleNotSetError(
                "You have not selected a main schedule, please choose one"
            )
        
        await self.storage.set_verification_code(
            user_id=user_id,
            code=code
        )
        
        await self.sender.send_verififaction_code(
            user_id=user_id,
            username=username,
            code=code
        )