from src.interfaces.web.schemas.login import LoginUserRequest

import pytest


def test_login_user_request_successfull():
    req = LoginUserRequest(email="test@example.com", password="123")
    
    assert req.email == "test@example.com"
    assert req.username is None
    assert req.password == "123"

    req2 = LoginUserRequest(username="user_username", password="123")

    assert req2.email is None 
    assert req2.username == "user_username"
    assert req2.password == "123"
    

def test_login_user_request_valueeror():
    with pytest.raises(ValueError):
        LoginUserRequest(password="123")