from fastapi import APIRouter


router = APIRouter()


@router.get("/register")
async def register():
    return {"detail": "User registered"}