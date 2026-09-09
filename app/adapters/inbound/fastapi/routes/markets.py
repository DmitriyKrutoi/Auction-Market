# app/adapters/inbound/fastapi/routes/api/markets.py
from datetime import datetime
from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4, BaseModel, Field

from app.adapters.inbound.fastapi.dependencies import (get_admin_user,
                                                       get_current_user,
                                                       get_uow)
from app.application.use_cases.create_market import (CreateMarket,
                                                     CreateMarketCommand)
from app.application.use_cases.list_market_bets import ListMarketBets
from app.application.use_cases.list_markets import ListMarkets
from app.application.use_cases.place_bet import PlaceBet, PlaceBetCommand
from app.application.use_cases.resolve_market import (ResolveMarket,
                                                      ResolveMarketCommand)
from app.domain.entities.user import User
from app.domain.exceptions import NotFoundError

router = APIRouter(prefix="/api/v1/markets", tags=["markets"])


class CreateMarketRequest(BaseModel):
    event_id: UUID4
    outcome: str
    odds: Decimal = Field(..., gt=1)


class MarketResponse(BaseModel):
    id: UUID4
    event_id: UUID4
    outcome: str
    odds: Decimal
    status: str
    total_bets_amount: Decimal


class BetRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)


class BetResponse(BaseModel):
    id: UUID4
    market_id: UUID4
    user_id: UUID4
    amount: Decimal
    odds: Decimal
    status: str
    potential_payout: Decimal
    created_at: datetime


class ResolveMarketRequest(BaseModel):
    winning_outcome: bool


class ResolveMarketResponse(BaseModel):
    resolved_bets: int
    winners: int
    losers: int


@router.post("", response_model=MarketResponse, status_code=status.HTTP_201_CREATED)
async def create_market(
    request: CreateMarketRequest,
    admin: User = Depends(get_admin_user),
    uow=Depends(get_uow),
):
    use_case = CreateMarket(uow)
    result = await use_case.execute(
        CreateMarketCommand(
            event_id=request.event_id, outcome=request.outcome, odds=request.odds
        )
    )
    return result


@router.get("", response_model=List[MarketResponse])
async def list_markets(event_id: UUID4 | None = None, uow=Depends(get_uow)):
    use_case = ListMarkets(uow)
    return await use_case.execute(event_id=event_id)


@router.get("/{market_id}", response_model=MarketResponse)
async def get_market(market_id: UUID4, uow=Depends(get_uow)):
    market = await uow.markets.get_by_id(market_id)
    if not market:
        raise NotFoundError(f"Рынок с id {market_id} не найден")
    return market


@router.post(
    "/{market_id}/bets", response_model=BetResponse, status_code=status.HTTP_201_CREATED
)
async def place_bet(
    market_id: UUID4,
    request: BetRequest,
    current_user: User = Depends(get_current_user),
    uow=Depends(get_uow),
):
    use_case = PlaceBet(uow)
    result = await use_case.execute(
        PlaceBetCommand(
            market_id=market_id, user_id=current_user.id, amount=request.amount
        )
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
    admin: User = Depends(get_admin_user),
    uow=Depends(get_uow),
):
    use_case = ResolveMarket(uow)
    result = await use_case.execute(
        ResolveMarketCommand(
            market_id=market_id,
            winning_outcome=request.winning_outcome,
            admin_id=admin.id,
        )
    )
    return result
