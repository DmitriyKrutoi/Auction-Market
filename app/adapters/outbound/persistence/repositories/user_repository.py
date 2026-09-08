from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.outbound.persistence.models import UserModel
from app.application.ports.repositories import UserRepository
from app.domain.entities.user import User
from app.domain.value_objects.wallet import Wallet


class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.get(UserModel, user_id)
        return self._to_domain(result) if result else None

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.scalar(stmt)
        return self._to_domain(result) if result else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.scalar(stmt)
        return self._to_domain(result) if result else None

    async def add(self, user: User) -> None:
        model = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            balance=user.wallet.balance,
            frozen=user.wallet.frozen,
            created_at=user.created_at,
            is_admin=user.is_admin,
        )
        self.session.add(model)
        await self.session.flush()

    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            wallet=Wallet(balance=model.balance, frozen=model.frozen),
            created_at=model.created_at,
            is_admin=model.is_admin,
        )
