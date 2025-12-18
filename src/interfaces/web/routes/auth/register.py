from fastapi import APIRouter


router = APIRouter()


@router.post("/register")
async def register():
    return {"detail": "User registered"}