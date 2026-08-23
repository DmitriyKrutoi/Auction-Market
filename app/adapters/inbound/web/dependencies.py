from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.adapters.inbound.fastapi.dependencies import token_service, async_session_factory
from app.adapters.outbound.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.domain.entities.user import User
import uuid


async def get_current_user_from_cookie(request: Request) -> User | None:
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
    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        user = await uow.users.get_by_id(user_id)
        return user


async def require_user(request: Request) -> User:
    """Требует авторизацию, иначе редирект на /login."""
    user = await get_current_user_from_cookie(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login?error=not_authenticated"}
        )
    return user