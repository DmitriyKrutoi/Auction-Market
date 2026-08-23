from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from decimal import Decimal
from app.domain.entities.user import User
from app.adapters.inbound.fastapi.dependencies import get_current_user
from app.adapters.inbound.fastapi.schemas.users import UserMeResponse
router = APIRouter(prefix="/users", tags=["users"])



@router.get("/me", response_model=UserMeResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserMeResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        balance=current_user.wallet.balance,
        frozen=current_user.wallet.frozen,
        created_at=current_user.created_at,
    )