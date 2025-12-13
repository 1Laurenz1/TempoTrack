import bcrypt


def hash_password(
    password: str
) -> bytes:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(rounds=12)
    )


def validate_password(
    password: str,
    hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )