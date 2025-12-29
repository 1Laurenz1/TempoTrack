from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserMeResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    tg_username: str | None
    created_at: datetime