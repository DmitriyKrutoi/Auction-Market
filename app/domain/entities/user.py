from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.value_objects.wallet import Wallet


@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    username: str = ""
    email: str = ""
    hashed_password: str = ""
    wallet: Wallet = field(default_factory=Wallet)
    created_at: datetime = field(default_factory=datetime.now)
    is_admin: bool = False

    @property
    def balance(self) -> int:
        return int(self.wallet.balance)

    @property
    def frozen(self) -> int:
        return int(self.wallet.frozen)
