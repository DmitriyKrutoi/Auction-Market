import uuid

import pytest

from app.adapters.inbound.fastapi.dependencies import (get_password_hasher,
                                                       get_token_service,
                                                       get_uow)
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.repositories import UserRepository
from app.application.ports.token_service import TokenService
from app.application.ports.unit_of_work import UnitOfWork
from app.main import app


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    async def get_by_id(self, user_id):
        return self.users.get(user_id)

    async def get_by_username(self, username):
        for u in self.users.values():
            if u.username == username:
                return u
        return None

    async def get_by_email(self, email):
        for u in self.users.values():
            if u.email == email:
                return u
        return None

    async def add(self, user):
        self.users[user.id] = user


class InMemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self.users = InMemoryUserRepository()
        self.committed = False
        self.rolled_back = False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()


class FakePasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed_{password}"

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return hashed_password == f"hashed_{plain_password}"


class FakeTokenService(TokenService):
    def create_access_token(self, user_id: uuid.UUID, username: str) -> str:
        return "fake_token"

    def decode_token(self, token: str) -> dict:
        return {"sub": str(uuid.uuid4()), "username": "testuser"}


@pytest.fixture(autouse=True)
def override_dependencies():
    fake_uow = InMemoryUnitOfWork()
    fake_hasher = FakePasswordHasher()
    fake_token = FakeTokenService()

    app.dependency_overrides[get_uow] = lambda: fake_uow
    app.dependency_overrides[get_password_hasher] = lambda: fake_hasher
    app.dependency_overrides[get_token_service] = lambda: fake_token

    yield {"uow": fake_uow, "hasher": fake_hasher, "token_service": fake_token}

    app.dependency_overrides.clear()
