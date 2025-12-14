from src.domain.entities.user import User
from src.infrastructure.database.models.user import UserModel

class UserMapper:
    @staticmethod
    def to_orm(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            tg_username=user.tg_username,
            telegram_id=user.telegram_id,
            schedules_count=user.schedules_count,
            main_schedule=user.main_schedule,
        )

    @staticmethod
    def to_domain(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password=user_model.password,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            tg_username=user_model.tg_username,
            telegram_id=user_model.telegram_id,
            schedules_count=user_model.schedules_count,
            main_schedule=user_model.main_schedule,
        )