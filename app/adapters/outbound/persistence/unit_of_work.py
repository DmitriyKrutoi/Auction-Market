# app/adapters/outbound/persistence/unit_of_work.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.application.ports.unit_of_work import UnitOfWork
from app.application.ports.repositories import UserRepository
from app.adapters.outbound.persistence.repositories.user_repository import PostgresUserRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.users: UserRepository | None = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = PostgresUserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()