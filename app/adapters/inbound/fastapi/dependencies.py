from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.adapters.outbound.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.application.dto.auth_principal import AuthPrincipal
from app.application.ports.token_service import TokenService
from app.application.services.auth_service import AuthService
from app.infrastructure.di.db import get_session_factory
from app.infrastructure.di.jwt_token_service import get_token_service


def get_auth_service(
    token_service: TokenService = Depends(get_token_service),
    session_factory=Depends(get_session_factory),
) -> AuthService:
    def uow_factory():
        return SqlAlchemyUnitOfWork(session_factory)

    return AuthService(token_service=token_service, uow_factory=uow_factory)


# Схема для получения токена из заголовка
bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    auth: AuthService = Depends(get_auth_service),
) -> AuthPrincipal:
    """Возвращает текущего пользователя или 401."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    principal = await auth.authenticate(credentials.credentials)
    if principal is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return principal
