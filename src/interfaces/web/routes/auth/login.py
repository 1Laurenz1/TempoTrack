from fastapi import APIRouter


router = APIRouter()


@router.get("/login")
async def register():
    return {"access_token": "jwt", "token_type": "bearer"}