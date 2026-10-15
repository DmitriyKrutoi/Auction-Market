from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AuthPrincipal:
    """Аутентифицированный пользователь в контексте запроса."""

    user_id: UUID
    username: str
    is_admin: bool
