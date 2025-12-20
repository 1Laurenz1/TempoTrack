from src.application.services.password_service import PasswordService


def get_password_service() -> PasswordService:
    return PasswordService()