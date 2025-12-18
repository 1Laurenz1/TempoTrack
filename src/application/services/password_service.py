import bcrypt


class PasswordService:
    def hash(self, password: str) -> bytes:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(rounds=12)
        )

    def verify(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password
        )