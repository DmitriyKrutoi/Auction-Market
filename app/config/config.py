from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    app_name: str = "Auction Market API"
    debug: bool = True

    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/auction_market"

    # JWT
    jwt_secret_key: str = "super-secret-key-change-in-prod"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Redis (позже)
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()