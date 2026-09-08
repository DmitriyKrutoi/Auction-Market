from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from app.adapters.inbound.fastapi.dependencies import get_admin_user, get_uow
from app.adapters.inbound.fastapi.schemas.events import (CreateEventRequest,
                                                         EventResponse,
                                                         ResolveEventRequest)
from app.application.use_cases.create_event import (CreateEvent,
                                                    CreateEventCommand)
from app.application.use_cases.list_events import ListEvents
from app.application.use_cases.resolve_event import (ResolveEvent,
                                                     ResolveEventCommand)
from app.domain.entities.user import User

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    request: CreateEventRequest,
    admin: User = Depends(get_admin_user),
    uow=Depends(get_uow),
):
    use_case = CreateEvent(uow)
    result = await use_case.execute(
        CreateEventCommand(
            title=request.title,
            description=request.description,
            category=request.category,
            outcomes=request.outcomes,
            admin_id=admin.id,
        )
    )
    return result


@router.get("", response_model=List[EventResponse])
async def list_events(uow=Depends(get_uow)):
    use_case = ListEvents(uow)
    return await use_case.execute()


@router.post("/{event_id}/resolve", response_model=EventResponse)
async def resolve_event(
    event_id: UUID4,
    request: ResolveEventRequest,
    admin: User = Depends(get_admin_user),
    uow=Depends(get_uow),
):
    use_case = ResolveEvent(uow)
    result = await use_case.execute(
        ResolveEventCommand(
            event_id=event_id,
            winning_outcome=request.winning_outcome,
            admin_id=admin.id,
        )
    )
    return result
