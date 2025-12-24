from fastapi import APIRouter


router = APIRouter()


@router.post("/schedules/create/")
async def create_schedule():
    ...