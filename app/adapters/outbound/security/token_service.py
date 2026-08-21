import jwt
from datetime import datetime, timedelta
from uuid import UUID
from app.application.ports.token_service import TokenService
from app.config.config import settings

class JwtTokenService(TokenService):
    def create_access_token(self, user_id: UUID, username: str) -> str:
        expire = datetime.now() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        payload = {
            "sub": str(user_id),
            "username": username,
            "exp": expire,
            "type": "access"
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])