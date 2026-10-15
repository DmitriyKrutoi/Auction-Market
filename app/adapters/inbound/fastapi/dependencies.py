import uuid

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.adapters.outbound.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.application.ports.token_service import TokenService
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.entities.user import User
from app.domain.exceptions import ForbiddenError
from app.infrastructure.di.jwt_token_service import get_token_service


def get_uow(request: Request) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(request.app.state.session_factory)


# Схема для получения токена из заголовка
bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    uow: UnitOfWork = Depends(get_uow),
    token_service: TokenService = Depends(get_token_service),
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
