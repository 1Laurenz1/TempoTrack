from pydantic import BaseModel


class VerificationAccountRequest(BaseModel):
    username: str
    
    
class VerificationAccountResponse(BaseModel):
    message: str
    
    
class VerifyCodeRequest(BaseModel):
    code: str
    
    
class VerifyCodeResponse(BaseModel):
    success: bool