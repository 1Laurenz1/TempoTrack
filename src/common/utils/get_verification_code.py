import secrets


def generate_verification_code() -> str:
    return secrets.token_hex(3)