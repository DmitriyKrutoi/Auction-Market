from app.adapters.outbound.security.token_service import JwtTokenService
from app.application.ports.token_service import TokenService
from app.config.config import settings


def get_token_service() -> TokenService:
    return JwtTokenService(
        secret=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expire_minutes=settings.jwt_access_token_expire_minutes,
    )
