# app/domain/value_objects/enums.py
from enum import Enum


class EventStatus(str, Enum):
    OPEN = "open"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"


class MarketStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class BetStatus(str, Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    RETURNED = "returned"
