from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.application.services.jwt_service import JwtService
from src.interfaces.web.dependencies.services import get_jwt_service


security = HTTPBearer()


def get_current_user_id(
    request: Request,
    jwt_service: JwtService = Depends(get_jwt_service),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = credentials.credentials

    try:
        payload = jwt_service.decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return int(payload["sub"])