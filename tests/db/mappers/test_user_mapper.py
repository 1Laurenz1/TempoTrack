import pytest

from src.domain.entities.user import User
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.mappers.user_mapper import UserMapper


def test_user_mapper_to_orm():
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password="hashed_password",
        first_name="Test",
        last_name="User",
        tg_username="tg_test",
        telegram_id=123456,
        schedules_count=2,
        main_schedule=1,
    )

    orm_user = UserMapper.to_orm(user)

    assert isinstance(orm_user, UserModel)

    assert orm_user.id == user.id
    assert orm_user.username == user.username
    assert orm_user.email == user.email
    assert orm_user.password == user.password
    assert orm_user.first_name == user.first_name
    assert orm_user.last_name == user.last_name
    assert orm_user.tg_username == user.tg_username
    assert orm_user.telegram_id == user.telegram_id
    assert orm_user.schedules_count == user.schedules_count
    assert orm_user.main_schedule == user.main_schedule