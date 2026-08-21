from abc import ABC, abstractmethod
from uuid import UUID


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, user_id: UUID, username: str) -> str:
        raise NotImplementedError


    @abstractmethod
    def decode_token(self, token: str) -> dict:
        raise NotImplementedError