from src.common.security.password import hash_password, validate_password

import pytest


def test_hash_and_verify_password():
    password = 'top-secret'
    
    hashed = hash_password(password)
    
    assert hashed != password
    assert validate_password(password, hashed) is True
    

def test_verify_password_wrong_password():
    hashed = hash_password("correct-password")
    
    assert validate_password("wrong-password", hashed) is False