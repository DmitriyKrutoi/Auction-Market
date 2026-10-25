from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from app.adapters.inbound.fastapi.dependencies import get_current_user
from app.adapters.inbound.fastapi.schemas.markets import (
    BetRequest,
    BetResponse,
    CreateMarketRequest,
    MarketResponse,
    ResolveMarketRequest,
    ResolveMarketResponse,
)
from app.application.dto.auth_principal import AuthPrincipal
from app.application.ports.unit_of_work import UnitOfWork
from app.application.use_cases.create_market import CreateMarket, CreateMarketCommand
from app.application.use_cases.get_market import GetMarket
from app.application.use_cases.list_market_bets import ListMarketBets
from app.application.use_cases.list_markets import ListMarkets
from app.application.use_cases.place_bet import PlaceBet, PlaceBetCommand
from app.application.use_cases.resolve_market import ResolveMarket, ResolveMarketCommand
from app.infrastructure.di.db import get_uow

router = APIRouter(prefix="/markets", tags=["markets"])


@router.post("", response_model=MarketResponse, status_code=status.HTTP_201_CREATED)
async def create_market(
    request: CreateMarketRequest,
    current_user: AuthPrincipal = Depends(get_current_user),  # ← AuthPrincipal
    uow: UnitOfWork = Depends(get_uow),
):
    use_case = CreateMarket(uow)
    result = await use_case.execute(
        command=CreateMarketCommand(
            event_id=request.event_id,
            outcome=request.outcome,
            odds=request.odds,
        ),
        actor=current_user,  # ← передаём AuthPrincipal
    )
    return result


@router.get("", response_model=List[MarketResponse])
async def list_markets(event_id: UUID4 | None = None, uow: UnitOfWork = Depends(get_uow)):
    use_case = ListMarkets(uow)
    return await use_case.execute(event_id=event_id)


@router.get("/{market_id}", response_model=MarketResponse)
async def get_market(
    market_id: UUID4,
    uow: UnitOfWork = Depends(get_uow),
):
    use_case = GetMarket(uow)
    return await use_case.execute(market_id=market_id)


@router.post("/{market_id}/bets", response_model=BetResponse, status_code=status.HTTP_201_CREATED)
async def place_bet(
    market_id: UUID4,
    request: BetRequest,
    current_user: AuthPrincipal = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    use_case = PlaceBet(uow)
    result = await use_case.execute(
        PlaceBetCommand(market_id=market_id, user_id=current_user.id, amount=request.amount)
    )
    return result


@router.get("/{market_id}/bets", response_model=List[BetResponse])
async def list_market_bets(market_id: UUID4, uow=Depends(get_uow)):
    use_case = ListMarketBets(uow)
    return await use_case.execute(market_id=market_id)


@router.post("/{market_id}/resolve", response_model=ResolveMarketResponse)
async def resolve_market(
    market_id: UUID4,
    request: ResolveMarketRequest,
    admin: AuthPrincipal = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    use_case = ResolveMarket(uow)
    result = await use_case.execute(
        ResolveMarketCommand(
            market_id=market_id,
            winning_outcome=request.winning_outcome,
        ),
        actor=admin,
    )
    return result
