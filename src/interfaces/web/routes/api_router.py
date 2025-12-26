from fastapi import APIRouter

from . import root
from .auth import (
    register,
    login
)
from .schedules import (
    schedule_create,
    set_main_schedule,
)


router = APIRouter()


router.include_router(root.router, tags=["Main"])
router.include_router(register.router, tags=["Auth"])
router.include_router(login.router, tags=["Auth"])
router.include_router(schedule_create.router, tags=["Schedules"])
router.include_router(set_main_schedule.router, tags=["Schedules"])