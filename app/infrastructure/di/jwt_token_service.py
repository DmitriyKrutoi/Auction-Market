from app.adapters.outbound.security.token_service import JwtTokenService
from app.application.ports.token_service import TokenService


def get_token_service() -> TokenService:
    return JwtTokenService()
