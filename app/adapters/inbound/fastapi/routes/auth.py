from fastapi import APIRouter, Depends, HTTPException, status

from app.adapters.inbound.fastapi.dependencies import (get_uow,
                                                       password_hasher,
                                                       token_service)
from app.adapters.inbound.fastapi.schemas.auth import (LoginRequest,
                                                       RegisterRequest,
                                                       RegisterResponse,
                                                       TokenResponse)
from app.adapters.outbound.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.application.dto.auth import AuthenticateUserCommand
from app.application.use_cases.authenticate_user import AuthenticateUser
from app.application.use_cases.register_user import (RegisterUser,
                                                     RegisterUserCommand)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    request: RegisterRequest, uow: SqlAlchemyUnitOfWork = Depends(get_uow)
):
    use_case = RegisterUser(uow, password_hasher)
    try:
        async with uow:
            result = await use_case.execute(
                RegisterUserCommand(
                    username=request.username,
                    email=request.email,
                    password=request.password,
                )
            )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, uow: SqlAlchemyUnitOfWork = Depends(get_uow)):
    use_case = AuthenticateUser(uow, password_hasher, token_service)
    try:
        async with uow:
            tokens = await use_case.execute(
                AuthenticateUserCommand(
                    username=request.username, password=request.password
                )
            )
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
