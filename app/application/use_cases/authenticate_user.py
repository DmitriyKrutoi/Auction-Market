from app.application.dto.auth import AuthenticateUserCommand, TokenPair
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.token_service import TokenService
from app.application.ports.unit_of_work import UnitOfWork


class AuthenticateUser:
    def __init__(
        self,
        uow: UnitOfWork,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def execute(self, command: AuthenticateUserCommand) -> TokenPair:
        user = await self.uow.users.get_by_username(command.username)
        if not user:
            raise ValueError("Неверное имя пользователя или пароль")
        if not self.password_hasher.verify(command.password, user.hashed_password):
            raise ValueError("Неверное имя пользователя или пароль")

        access_token = self.token_service.create_access_token(user.id, user.username)
        return TokenPair(access_token=access_token)
