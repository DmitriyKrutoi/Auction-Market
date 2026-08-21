from abc import ABC, abstractmethod
from app.application.ports.repositories import UserRepository

class UnitOfWork(ABC):
    users: UserRepository

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError