import uuid

from fastapi import Depends, HTTPException, Request, status

from app.adapters.outbound.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.application.ports.token_service import TokenService
from app.domain.entities.user import User
from app.infrastructure.auth.jwt_token_service import get_token_service


async def get_current_user_from_cookie(
    request: Request,
    token_service: TokenService = Depends(get_token_service),
) -> User | None:
    """Получает пользователя из JWT-токена в cookie."""
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        # Декодируем токен
        payload = token_service.decode_token(token)
        user_id = uuid.UUID(payload.get("sub"))
    except Exception:
        return None

    # Загружаем пользователя из БД
    async with SqlAlchemyUnitOfWork(request.app.state.session_factory) as uow:
        user = await uow.users.get_by_id(user_id)
        return user


async def require_user(request: Request) -> User:
    """Требует авторизацию, иначе редирект на /login."""
    user = await get_current_user_from_cookie(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login?error=not_authenticated"},
        )
    return user


def get_csrf_token(request: Request) -> str:
    return request.cookies.get("csrf_token", "")


async def require_admin(request: Request):
    """Требует авторизацию + права админа."""
    user = await require_user(request)  # переиспользуем проверку авторизации
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/?error=forbidden"},
        )
    return user
