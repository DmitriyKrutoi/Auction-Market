from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from decimal import Decimal

class UserMeResponse(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    balance: Decimal
    frozen: Decimal
    created_at: datetime