import secrets


def verify_verification_code(
    code: str,
    entered_code: str    
) -> bool:
    return secrets.compare_digest(code, entered_code)