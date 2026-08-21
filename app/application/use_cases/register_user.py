from dataclasses import dataclass
from uuid import UUID
from app.application.ports.repositories import UserRepository
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.entities.user import User
from app.domain.value_objects.wallet import Wallet
from decimal import Decimal


@dataclass
class RegisterUserCommand:
    username: str
    email: str
    password: str

@dataclass
class RegisterUserResponse:
    user_id: UUID
    username: str
    email: str

class RegisterUser:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher):
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, command: RegisterUserCommand) -> RegisterUserResponse:
        # Проверка уникальности username и email
        if await self.uow.users.get_by_username(command.username):
            raise ValueError("Пользователь с таким именем уже существует")
        if await self.uow.users.get_by_email(command.email):
            raise ValueError("Пользователь с таким email уже существует")

        hashed_password = self.password_hasher.hash(command.password)
        user = User(
            username=command.username,
            email=command.email,
            hashed_password=hashed_password,
            wallet=Wallet(balance=Decimal("1000"))  # стартовый бонус
        )
        await self.uow.users.add(user)
        await self.uow.commit()

        return RegisterUserResponse(
            user_id=user.id,
            username=user.username,
            email=user.email
        )