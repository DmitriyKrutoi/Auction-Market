import bcrypt

from passlib.context import CryptContext
from app.application.ports.password_hasher import PasswordHasher

class BcryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        # bcrypt работает только с байтами и принимает максимум 72 байта.
        # Обрезаем вручную, чтобы избежать исключения.
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        password_bytes = plain_password.encode('utf-8')[:72]
        return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))