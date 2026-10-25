from fastapi import APIRouter, Depends, status

from app.adapters.inbound.fastapi.dependencies import get_uow, password_hasher, token_service
from app.adapters.inbound.fastapi.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.application.dto.auth import AuthenticateUserCommand
from app.application.ports.unit_of_work import UnitOfWork
from app.application.use_cases.authenticate_user import AuthenticateUser
from app.application.use_cases.register_user import RegisterUser, RegisterUserCommand

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, uow: UnitOfWork = Depends(get_uow)):
    use_case = RegisterUser(uow, password_hasher)
    result = await use_case.execute(
        RegisterUserCommand(
            username=request.username,
            email=request.email,
            password=request.password,
        )
    )
    return result


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, uow: UnitOfWork = Depends(get_uow)):
    use_case = AuthenticateUser(uow, password_hasher, token_service)

    tokens = await use_case.execute(
        AuthenticateUserCommand(username=request.username, password=request.password)
    )
    return tokens
