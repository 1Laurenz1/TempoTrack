import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.web.routes.auth.register import router
from src.interfaces.web.dependencies.usecases import get_register_user_usecase

from src.application.usecases.register_user import RegisterUserUseCase
from src.application.services.password_service import PasswordService

from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.exceptions.infrastructure_error import InfrastructureError


@pytest.mark.asyncio
async def test_register_user_with_test_db(db_session: AsyncSession):
    password_service = PasswordService()
    user_repository = UserRepositoryImpl(session=db_session)
    register_usecase = RegisterUserUseCase(
        user_repository=user_repository,
        password_service=password_service
    )

    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_register_user_usecase] = lambda: register_usecase

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:

        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword",
            "first_name": "Test",
            "last_name": "User"
        }

        response = await ac.post("/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"

    created_user = await user_repository.get_user_by_email(payload["email"])
    assert created_user is not None
    assert created_user.username == "testuser"
    

@pytest.mark.asyncio
async def test_user_already_exists_error(db_session: AsyncSession):
    password_service = PasswordService()
    user_repository = UserRepositoryImpl(session=db_session)
    register_usecase = RegisterUserUseCase(
        user_repository=user_repository,
        password_service=password_service
    )

    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_register_user_usecase] = lambda: register_usecase

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:

        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword",
            "first_name": "Test",
            "last_name": "User"
        }

        response = await ac.post("/register", json=payload)
        assert response.status_code == 200
        
        response = await ac.post("/register", json=payload)
        assert response.status_code == 400
        
        
@pytest.mark.asyncio
async def test_register_user_infrastructure_error():
    class FailingUserRepository(UserRepositoryImpl):
        async def add(self, user):
            raise InfrastructureError("DB error")
    
    password_service = PasswordService()
    failing_repo = FailingUserRepository(session=None)
    register_usecase = RegisterUserUseCase(
        user_repository=failing_repo,
        password_service=password_service
    )

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_register_user_usecase] = lambda: register_usecase

    from httpx import AsyncClient, ASGITransport

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:

        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword",
            "first_name": "Test",
            "last_name": "User"
        }

        response = await ac.post("/register", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"