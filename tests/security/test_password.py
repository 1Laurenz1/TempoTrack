from src.application.services.password_service import PasswordService

import pytest


def test_hash_and_verify_password():
    password_service = PasswordService()
    
    password = 'top-secret'
    
    hashed = password_service.hash(password)
    
    assert hashed != password
    assert password_service.verify(password, hashed) is True
    

def test_verify_password_wrong_password():
    password_service = PasswordService()
    
    hashed = password_service.hash("correct-password")
    
    assert password_service.verify("wrong-password", hashed) is False