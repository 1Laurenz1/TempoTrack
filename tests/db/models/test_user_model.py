import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.user import UserModel

import pytest   
import pytest_asyncio
from src.application.services.password_service import PasswordService


@pytest.mark.asyncio
async def test_user_creation_orm(db_session):
    password_manager = PasswordService()
    user = UserModel(
        username="John",
        email="john@example.com",
        password=password_manager.hash("secret"),
        first_name="John",
        last_name="Alderson",
        tg_username="JohnAlderson",
        telegram_id=1846256732,
        schedules_count=3,
        main_schedule=2
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.id is not None
    assert user.username == "John"
    assert user.email == "john@example.com"
    assert password_manager.verify("secret", user.password) is True
    assert user.first_name == "John"
    assert user.last_name == "Alderson"
    assert user.tg_username == "JohnAlderson"
    assert user.telegram_id == 1846256732
    assert user.schedules_count == 3
    assert user.main_schedule == 2
    
    assert user.is_active is True
    
    user.schedules_count = 0
    assert user.is_active is False
    
    result = user.full_name
    assert result == "John Alderson"
    
    user_db = await db_session.get(UserModel, user.id)
    assert user_db is not None