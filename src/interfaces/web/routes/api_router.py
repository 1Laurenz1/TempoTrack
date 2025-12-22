from fastapi import APIRouter

from . import root
from .auth import (
    register,
    login
)


router = APIRouter()


router.include_router(root.router, tags=["Main"])
router.include_router(register.router, tags=["Auth"])
router.include_router(login.router, tags=["Auth"])