import pytest
from datetime import datetime

from src.domain.entities.user import User
from src.application.services.password_service import PasswordService


def test_user_creation():
    password_manager = PasswordService()
    user = User(
        username="john",
        email="john@example.com",
        password=password_manager.hash("123"),
        first_name="John",
        last_name="Doe",
        tg_username="@john",
        telegram_id=12345,
        schedules_count=2,
        main_schedule=10,
    )

    assert user.username == "john"
    assert user.email == "john@example.com"
    assert password_manager.verify("123", user.password) is True
    assert user.telegram_id == 12345
    assert user.schedules_count == 2
    assert user.main_schedule == 10
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    

def test_user_is_active():
    user = User(schedules_count=0)
    assert user.is_active is False

    user.schedules_count = 1
    assert user.is_active is True
    
    
def test_user_info_about_user():
    user = User(username="a", email="b", tg_username="c", telegram_id=5)
    result = user.info_about_user
    assert "a b c 5" in result