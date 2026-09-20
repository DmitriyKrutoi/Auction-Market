from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from app.domain.exceptions import EventNotOpenError, InvalidOperationError, ValidationError
from app.domain.value_objects.enums import EventStatus


@dataclass
class Event:
    title: str
    description: str = ""
    category: str = ""
    status: EventStatus = EventStatus.OPEN
    id: UUID = field(default_factory=uuid4)
    outcomes: List[str] = field(
        default_factory=list
    )  # например, ["Команда A", "Команда B", "Ничья"]
    resolved_outcome: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: datetime | None = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.title or not self.title.strip():
            raise ValidationError("Название события обязательно")
        if not self.outcomes or len(self.outcomes) < 2:
            raise ValidationError("Должно быть минимум 2 исхода")
        if len(self.outcomes) != len(set(self.outcomes)):
            raise ValidationError("Исходы не должны содержать дубликатов")

    def resolve(self, outcome: str):
        if self.status != EventStatus.OPEN:
            raise EventNotOpenError(f"Событие не открыто: {self.status}")
        if outcome not in self.outcomes:
            raise InvalidOperationError(f"Неверный исход: {outcome}")
        self.status = EventStatus.RESOLVED
        self.resolved_outcome = outcome
        self.resolved_at = datetime.now()

    def cancel(self):
        """Отменяет событие."""
        if self.status != EventStatus.OPEN:
            raise EventNotOpenError(f"Событие не открыто: {self.status}")
        self.status = EventStatus.CANCELLED
