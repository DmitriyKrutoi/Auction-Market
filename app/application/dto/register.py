from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RegisterUserCommand:
    username: str
    email: str
    password: str


@dataclass(frozen=True)
class RegisterUserResponse:
    user_id: UUID
    username: str
    email: str
