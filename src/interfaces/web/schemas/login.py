from typing import Optional
from pydantic import BaseModel, EmailStr, model_validator


class LoginUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str
    
    
    @model_validator(mode="after")
    def check_email_or_username(cls, values):
        email, username = values.email, values.username
        
        if not email and not username:
            raise ValueError("Either email or username must be provided")
        return values


    
class LoginUserResponse(BaseModel):
    email: EmailStr
    username: str