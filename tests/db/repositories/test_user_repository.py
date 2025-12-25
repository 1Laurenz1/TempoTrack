import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.exceptions.user_already_exists_error import (
    UserAlreadyExistsError
)
from src.application.services.password_service import PasswordService


@pytest.mark.asyncio
async def test_add_user_success(db_session: AsyncSession):
    user_repository = UserRepositoryImpl(db_session)
    password_manager = PasswordService()
    user = User(
        username="john",
        email="john@example.com",
        password=password_manager.hash("hashed-password"),
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=1,
        main_schedule=1
    )

    result = await user_repository.add(user)

    assert result is not None
    assert result.id is not None
    assert result.email == user.email
    assert result.username == user.username


@pytest.mark.asyncio
async def test_add_user_already_exists(db_session: AsyncSession):
    user_repository = UserRepositoryImpl(db_session)
    password_manager = PasswordService()
    
    user = User(
        username="john",
        email="john@example.com",
        password=password_manager.hash("hashed-password"),
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=1,
        main_schedule=1
    )

    await user_repository.add(user)

    with pytest.raises(UserAlreadyExistsError):
        await user_repository.add(user)


@pytest.mark.asyncio
async def test_get_user_by_email_success(db_session: AsyncSession):
    user_repository = UserRepositoryImpl(db_session)
    password_manager = PasswordService()

    
    user = User(
        username="john",
        email="john@example.com",
        password=password_manager.hash("hashed-password"),
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=1,
        main_schedule=1
    )

    await user_repository.add(user)

    result = await user_repository.get_user_by_email("john@example.com")

    assert result is not None
    assert result.email == "john@example.com"
    assert result.username == "john"


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(db_session: AsyncSession):
    user_repository = UserRepositoryImpl(db_session)
    
    result = await user_repository.get_user_by_email("notfound@example.com")

    assert result is None
    

@pytest.mark.asyncio
async def test_increment_schedules_count(
    db_session: AsyncSession
):
    user_repository = UserRepositoryImpl(db_session)
  
    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=0,
        main_schedule=None
    )
    
    user = await user_repository.add(user)
    
    assert user.schedules_count == 0

    await user_repository.increment_schedules_count(user.id)

    user_from_db = await db_session.get(UserModel, user.id)
    assert user_from_db.schedules_count == 1


@pytest.mark.asyncio
async def test_decrement_schedules_count(
    db_session: AsyncSession
):
    user_repository = UserRepositoryImpl(db_session)
  
    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=2,
        main_schedule=None
    )
    
    user = await user_repository.add(user)
    
    user.schedules_count = 2
    await db_session.commit()

    await user_repository.decrement_schedules_count(user.id)

    user_from_db = await db_session.get(UserModel, user.id)
    assert user_from_db.schedules_count == 1


@pytest.mark.asyncio
async def test_decrement_schedules_count_does_not_go_below_zero(
    db_session: AsyncSession,
):
    user_repository = UserRepositoryImpl(db_session)
  
    user = User(
        username="john",
        email="john@example.com",
        password=b"hashed-password",
        first_name="John",
        last_name="Doe",
        tg_username="john_doe",
        telegram_id=123456789,
        schedules_count=0,
        main_schedule=None
    )
    
    user = await user_repository.add(user)
    
    assert user.schedules_count == 0

    await user_repository.decrement_schedules_count(user.id)

    user_from_db = await db_session.get(UserModel, user.id)
    assert user_from_db.schedules_count == 0