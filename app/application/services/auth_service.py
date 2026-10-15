from uuid import UUID

from jwt import InvalidTokenError

from app.application.dto.auth_principal import AuthPrincipal


class AuthService:
    async def authenticate(self, token: str | None) -> AuthPrincipal | None:
        if not token:
            return None

        user_id = self._decode_user_id(token)
        if user_id is None:
            return None

        return await self._load_principal(user_id)

    def _decode_user_id(self, token: str) -> UUID | None:

        try:
            payload = self.token_service.decode_token(token)
            return UUID(payload["sub"])
        except (InvalidTokenError, KeyError, ValueError):
            return None

    async def _load_principal(self, user_id: UUID) -> AuthPrincipal | None:
        async with self.uow_factory() as uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                return None
            return AuthPrincipal(
                user_id=user.id,
                username=user.username,
                is_admin=user.is_admin,
            )
