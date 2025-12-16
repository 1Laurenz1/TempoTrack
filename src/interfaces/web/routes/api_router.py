from fastapi import APIRouter

from . import root


router = APIRouter()


router.include_router(root.router, tags=["Main"])