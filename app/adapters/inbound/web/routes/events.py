import httpx
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.adapters.inbound.web.dependencies import get_csrf_token, require_admin, require_user

router = APIRouter(prefix="/events", tags=["web-events"])

templates = Jinja2Templates(directory="app/adapters/inbound/web/templates")

API_BASE_URL = "http://localhost:8000/api/v1"


@router.get("", response_class=HTMLResponse)
async def events_list(
    request: Request,
    current_user: dict = Depends(require_user),
    csrf_token: str = Depends(get_csrf_token),
):
    """Список событий."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/events")

    events = response.json() if response.status_code == 200 else []

    print(current_user)

    return templates.TemplateResponse(
        request=request,
        name="events/list.html",
        context={
            "title": "События",
            "events": events,
            "csrf_token": csrf_token,
            "current_user": current_user,
        },
    )


@router.get("/create", response_class=HTMLResponse)
async def create_event_page(
    request: Request,
    admin=Depends(require_admin),  # ← защита: только админ
    csrf_token: str = Depends(get_csrf_token),
):
    """Форма создания события. Доступна только админу."""
    return templates.TemplateResponse(
        request=request,
        name="events/create.html",
        context={"title": "Создать событие", "current_user": admin, "csrf_token": csrf_token},
    )


@router.post("/create")
async def create_event_form(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    category: str = Form(""),
    outcomes: str = Form(...),
    admin=Depends(require_admin),
    csrf_token: str = Form(...),
):
    """Обработка формы создания события."""
    # 1. CSRF-проверка — ПЕРВОЙ
    cookie_token = request.cookies.get("csrf_token")
    if not cookie_token or csrf_token != cookie_token:
        raise HTTPException(403, "CSRF token mismatch")

    # 2. Парсим данные
    outcomes_list = [o.strip() for o in outcomes.split(",") if o.strip()]
    token = request.cookies.get("access_token")

    # 3. Вызываем API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/events",
            json={
                "title": title,
                "description": description,
                "category": category,
                "outcomes": outcomes_list,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

    # 4. Успех — редирект
    if response.status_code == 201:
        return RedirectResponse(url="/events", status_code=303)

    # 5. Ошибка — возвращаем форму
    if response.headers.get("content-type", "").startswith("application/json"):
        error_detail = response.json().get("detail", "Ошибка создания события")
    else:
        error_detail = "Внутренняя ошибка сервера"

    return templates.TemplateResponse(
        request=request,
        name="events/create.html",
        context={
            "title": "Создать событие",
            "current_user": admin,
            "csrf_token": csrf_token,  # ← важно
            "error": error_detail,
            "form_data": {
                "title": title,
                "description": description,
                "category": category,
                "outcomes": outcomes,
            },
        },
        status_code=status.HTTP_200_OK,  # ← 200, не 500
    )


@router.post("/{event_id}/resolve")
async def resolve_event_form(
    request: Request,
    event_id: str,
    winning_outcome: str = Form(...),
    admin=Depends(require_admin),
    csrf_token: str = Form(...),
):
    """Обработка формы разрешения события."""
    # 1. CSRF-проверка
    cookie_token = request.cookies.get("csrf_token")
    if not cookie_token or csrf_token != cookie_token:
        raise HTTPException(403, "CSRF token mismatch")

    # 2. Достаём JWT
    token = request.cookies.get("access_token")

    # 3. Вызываем API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/events/{event_id}/resolve",
            json={"winning_outcome": winning_outcome},
            headers={"Authorization": f"Bearer {token}"},
        )

    # 4. Редирект обратно на список (с флагом успеха/ошибки)
    if response.status_code == 200:
        return RedirectResponse(
            url="/events?resolved=true",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return RedirectResponse(
        url="/events?error=resolve_failed",
        status_code=status.HTTP_303_SEE_OTHER,
    )
