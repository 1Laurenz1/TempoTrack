import pytest

from src.application.services.jwt_service import JwtService
from src.application.exceptions.auth import InvalidTokenError


def test_jwt_encode_decode():
    service = JwtService(
        secret_key="testkey", algorithm="HS256", access_token_ttl_minutes=1
    )
    
    payload = {"user_id": 123}
    token = service.create_access_token(payload)
    
    decoded = service.decode_token(token)
    
    assert decoded["user_id"] == 123
    assert "exp" in decoded
    

def test_invalid_token_error():
    service = JwtService(
        secret_key="testkey", algorithm="HS256", access_token_ttl_minutes=1
    )
    
    with pytest.raises(InvalidTokenError):
        service.decode_token("invalid.token.value")