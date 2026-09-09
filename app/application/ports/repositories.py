from abc import ABC, abstractmethod
from uuid import UUID

from app.application.dto.bet_summary import UserBetSummary
from app.domain.entities.bet import Bet
from app.domain.entities.event import Event
from app.domain.entities.market import Market
from app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError


class EventRepository(ABC):
    @abstractmethod
    async def get_by_id(self, event_id: UUID) -> Event | None: ...
    @abstractmethod
    async def add(self, event: Event) -> None: ...
    @abstractmethod
    async def list_open(self) -> list[Event]: ...


class MarketRepository(ABC):
    @abstractmethod
    async def get_by_id(self, market_id: UUID) -> Market | None: ...
    @abstractmethod
    async def add(self, market: Market) -> None: ...
    @abstractmethod
    async def list_by_event(self, event_id: UUID) -> list[Market]: ...
    @abstractmethod
    async def list_open(self) -> list[Market]: ...


class BetRepository(ABC):
    @abstractmethod
    async def get_by_id(self, bet_id: UUID) -> Bet | None: ...
    @abstractmethod
    async def add(self, bet: Bet) -> None: ...
    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Bet]: ...
    @abstractmethod
    async def list_by_market(self, market_id: UUID) -> list[Bet]: ...
    @abstractmethod
    async def list_pending_by_market(self, market_id: UUID) -> list[Bet]: ...

    @abstractmethod
    async def get_winners_summary(self, market_id: UUID) -> list[UserBetSummary]:
        """Получает агрегированную информацию по ставкам."""
        raise NotImplementedError
