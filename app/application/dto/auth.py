from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticateUserCommand:
    username: str
    password: str


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    token_type: str = "bearer"
