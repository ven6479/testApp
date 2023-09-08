from passlib.hash import bcrypt


class PasswordManager:
    @staticmethod
    async def hash_password(password: str) -> str:
        hashed_password = bcrypt.hash(password)
        return hashed_password

    @staticmethod
    async def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)
