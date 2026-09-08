# app/adapters/inbound/fastapi/dependencies.py
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.adapters.outbound.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.adapters.outbound.security.password_hasher import BcryptPasswordHasher
from app.adapters.outbound.security.token_service import JwtTokenService
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.token_service import TokenService
from app.application.ports.unit_of_work import UnitOfWork
from app.config.config import settings
from app.domain.entities.user import User
from app.domain.exceptions import ForbiddenError

engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


def get_uow() -> UnitOfWork:
    return SqlAlchemyUnitOfWork(async_session_factory)


def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


def get_token_service() -> TokenService:
    JwtTokenService()


password_hasher = BcryptPasswordHasher()
token_service = JwtTokenService()

# Схема для получения токена из заголовка
bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    uow: UnitOfWork = Depends(get_uow),
):
    token = credentials.credentials
    try:
        payload = token_service.decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with uow:
        user = await uow.users.get_by_id(user_uuid)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Проверяет, что пользователь является администратором."""
    if not current_user.is_admin:
        raise ForbiddenError("Требуются права администратора")
    return current_user
