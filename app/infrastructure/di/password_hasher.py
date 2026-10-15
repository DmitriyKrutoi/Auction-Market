from app.adapters.outbound.security.password_hasher import BcryptPasswordHasher
from app.application.ports.password_hasher import PasswordHasher


def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()
