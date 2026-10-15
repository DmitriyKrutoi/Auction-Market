from uuid import UUID

from app.application.dto.auth_principal import AuthPrincipal
from app.domain.exceptions import ForbiddenError


def require_admin(principal: AuthPrincipal) -> None:
    """Проверяет, что principal — админ.

    Бросает PermissionDeniedError, если нет.
    """
    if not principal.is_admin:
        raise ForbiddenError("Требуются права администратора")


def require_owner(principal: AuthPrincipal, owner_id: UUID) -> None:
    """Проверяет, что principal — владелец ресурса (или админ).

    Бросает PermissionDeniedError, если нет.
    """
    if principal.user_id != owner_id and not principal.is_admin:
        raise ForbiddenError("Требуются права владельца")


def require_self_or_admin(principal: AuthPrincipal, user_id: UUID) -> None:
    """Проверяет, что principal действует от своего имени или он админ."""
    if principal.user_id != user_id and not principal.is_admin:
        raise ForbiddenError("Можно действовать только от своего имени")
