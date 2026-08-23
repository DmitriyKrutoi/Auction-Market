from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import status
from app.adapters.inbound.web.dependencies import require_user, get_current_user_from_cookie
from app.domain.entities.user import User

router = APIRouter(tags=["web-pages"])

templates = Jinja2Templates(directory="app/adapters/inbound/web/templates")


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    current_user: User | None = Depends(get_current_user_from_cookie)
):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={
            "title": "Главная",
            "current_user": current_user
        }
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request,
    current_user: User = Depends(require_user)
):
    return templates.TemplateResponse(
        name="profile.html",
        request=request,
        context={
            "title": "Профиль",
            "current_user": current_user,
            "user": current_user
        }
    )