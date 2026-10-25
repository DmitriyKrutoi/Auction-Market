from fastapi import APIRouter, Depends

from app.adapters.inbound.fastapi.dependencies import get_current_user
from app.adapters.inbound.fastapi.schemas.users import UserMeResponse
from app.application.dto.auth_principal import AuthPrincipal
from app.application.ports.unit_of_work import UnitOfWork
from app.application.use_cases.get_user_profile import GetUserProfile
from app.infrastructure.di.db import get_uow

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserMeResponse)
async def read_users_me(
    current_user: AuthPrincipal = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    use_case = GetUserProfile(uow)
    return await use_case.execute(user_id=current_user.user_id)
