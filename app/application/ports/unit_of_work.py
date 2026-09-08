from abc import ABC, abstractmethod

from app.application.ports.repositories import (BetRepository, EventRepository,
                                                MarketRepository,
                                                UserRepository)


class UnitOfWork(ABC):
    users: UserRepository
    events: EventRepository
    markets: MarketRepository
    bets: BetRepository

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
