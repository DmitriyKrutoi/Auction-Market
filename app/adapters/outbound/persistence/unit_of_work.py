from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.adapters.outbound.persistence.repositories.bet_repository import \
    PostgresBetRepository
from app.adapters.outbound.persistence.repositories.event_repository import \
    PostgresEventRepository
from app.adapters.outbound.persistence.repositories.market_repository import \
    PostgresMarketRepository
from app.adapters.outbound.persistence.repositories.user_repository import \
    PostgresUserRepository
from app.application.ports.repositories import (BetRepository, EventRepository,
                                                MarketRepository,
                                                UserRepository)
from app.application.ports.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.users: UserRepository | None = None
        self.events: EventRepository | None = None
        self.markets: MarketRepository | None = None
        self.bets: BetRepository | None = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = PostgresUserRepository(self.session)
        self.events = PostgresEventRepository(self.session)
        self.markets = PostgresMarketRepository(self.session)
        self.bets = PostgresBetRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
