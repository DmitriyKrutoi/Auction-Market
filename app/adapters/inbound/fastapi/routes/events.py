from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from app.adapters.inbound.fastapi.dependencies import get_current_user
from app.adapters.inbound.fastapi.schemas.events import (
    CreateEventRequest,
    EventResponse,
    ResolveEventRequest,
)
from app.application.dto.auth_principal import AuthPrincipal
from app.application.ports.unit_of_work import UnitOfWork
from app.application.use_cases.create_event import CreateEvent, CreateEventCommand
from app.application.use_cases.list_events import ListEvents
from app.application.use_cases.resolve_event import ResolveEvent, ResolveEventCommand
from app.infrastructure.di.db import get_uow

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    request: CreateEventRequest,
    current_user: AuthPrincipal = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    use_case = CreateEvent(uow)
    result = await use_case.execute(
        CreateEventCommand(
            title=request.title,
            description=request.description,
            category=request.category,
            outcomes=request.outcomes,
        ),
        actor=current_user,
    )
    return result


@router.get("", response_model=List[EventResponse])
async def list_events(uow: UnitOfWork = Depends(get_uow)):
    use_case = ListEvents(uow)
    return await use_case.execute()


@router.post("/{event_id}/resolve", response_model=EventResponse)
async def resolve_event(
    event_id: UUID4,
    request: ResolveEventRequest,
    current_user: AuthPrincipal = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    use_case = ResolveEvent(uow)
    result = await use_case.execute(
        ResolveEventCommand(
            event_id=event_id,
            winning_outcome=request.winning_outcome,
        ),
        actor=current_user,
    )
    return result
