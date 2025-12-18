from typing import Optional
from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    
class RegisterUserResponse(BaseModel):
    email: EmailStr
    username: str
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None