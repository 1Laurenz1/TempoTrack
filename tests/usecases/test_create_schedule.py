import pytest
from unittest.mock import AsyncMock

from src.application.usecases.create_schedule import CreateScheduleUseCase
from src.application.dto.schedule import ScheduleCreateRequest
from src.application.exceptions.auth import UserNotFoundError

from src.domain.entities.schedule import Schedule
from src.domain.value_objects.schedule_types import ScheduleTypes


@pytest.mark.asyncio
async def test_create_schedule_success():
    user_repo = AsyncMock()
    schedule_repo = AsyncMock()

    user_repo.get_user_by_id.return_value = object()

    created_schedule = Schedule(
        id=1,
        user_id=42,
        name="My schedule",
        description="Test description",
        type_schedule=ScheduleTypes.DAILY,
    )

    schedule_repo.create.return_value = created_schedule

    usecase = CreateScheduleUseCase(
        user_repository=user_repo,
        schedule_repository=schedule_repo,
    )

    data = ScheduleCreateRequest(
        name="My schedule",
        description="Test description",
        type_schedule=ScheduleTypes.DAILY,
    )

    result = await usecase.execute(data=data, user_id=42)

    assert result.id == 1
    assert result.name == "My schedule"
    assert result.description == "Test description"
    assert result.type_schedule == ScheduleTypes.DAILY

    user_repo.get_user_by_id.assert_awaited_once_with(42)

    schedule_repo.create.assert_awaited_once()
    created_arg = schedule_repo.create.call_args.args[0]

    assert isinstance(created_arg, Schedule)
    assert created_arg.user_id == 42
    assert created_arg.name == data.name



@pytest.mark.asyncio
async def test_create_schedule_user_not_found():
    user_repo = AsyncMock()
    schedule_repo = AsyncMock()

    user_repo.get_user_by_id.return_value = None

    usecase = CreateScheduleUseCase(
        user_repository=user_repo,
        schedule_repository=schedule_repo,
    )

    data = ScheduleCreateRequest(
        name="Schedule",
        type_schedule=ScheduleTypes.DAILY,
    )

    with pytest.raises(UserNotFoundError):
        await usecase.execute(data=data, user_id=999)

    user_repo.get_user_by_id.assert_awaited_once_with(999)
    schedule_repo.create.assert_not_called()
