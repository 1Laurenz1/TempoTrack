from fastapi import APIRouter

from . import root
from .auth import (
    register,
)


router = APIRouter()


router.include_router(root.router, tags=["Main"])
router.include_router(register.router, tags=["Auth"])