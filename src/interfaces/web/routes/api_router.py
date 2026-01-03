from fastapi import APIRouter

from . import root
from .auth import (
    register,
    login
)
from .schedules import (
    schedule_create,
    set_main_schedule,
    add_item_schedule
)
from .user import (
    get_me,
    get_my_schedules
)
from .verify_account import verify


router = APIRouter()


router.include_router(root.router, tags=["Main"])
router.include_router(register.router, tags=["Auth"])
router.include_router(login.router, tags=["Auth"])
router.include_router(schedule_create.router, tags=["Schedules"])
router.include_router(set_main_schedule.router, tags=["Schedules"])
router.include_router(add_item_schedule.router, tags=["Schedules"])
router.include_router(get_me.router, tags=["Users"])
router.include_router(get_my_schedules.router, tags=["Users"])
router.include_router(verify.router, tags=["Verify"])