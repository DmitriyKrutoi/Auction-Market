from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.adapters.inbound.web.dependencies import get_current_user_from_cookie, require_user
from app.domain.entities.user import User

router = APIRouter(tags=["web-pages"])

templates = Jinja2Templates(directory="app/adapters/inbound/web/templates")


@router.get("/home", response_class=HTMLResponse)
async def index(
    request: Request, current_user: User | None = Depends(get_current_user_from_cookie)
):
    return templates.TemplateResponse(
        name="user/index.html",
        request=request,
        context={"title": "Главная", "current_user": current_user},
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, current_user: User = Depends(require_user)):
    return templates.TemplateResponse(
        name="user/profile.html",
        request=request,
        context={"title": "Профиль", "current_user": current_user, "user": current_user},
    )
