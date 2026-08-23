from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import status
import httpx

router = APIRouter(tags=["web-auth"])

templates = Jinja2Templates(directory="app/adapters/inbound/web/templates")

# URL внутреннего API
API_BASE_URL = "http://localhost:8000/api/v1"


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"title": "Регистрация"}
    )


@router.post("/register")
async def register_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
    
    if response.status_code == 201:
        return RedirectResponse(
            url="/login?registered=true",
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        error_detail = response.json().get("detail", "Ошибка регистрации")
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"title": "Регистрация", "error": error_detail},
            status_code=response.status_code
        )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, registered: bool = False):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "title": "Вход",
            "registered": registered
        }
    )


@router.post("/login")
async def login_form(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": username, "password": password}
        )
    
    if response.status_code == 200:
        token_data = response.json()
        # Сохраняем токен в cookie
        redirect = RedirectResponse(
            url="/profile",
            status_code=status.HTTP_303_SEE_OTHER
        )
        redirect.set_cookie(
            key="access_token",
            value=token_data["access_token"],
            httponly=True,
            max_age=1800,  # 30 минут
            samesite="lax"
        )
        return redirect
    else:
        error_detail = response.json().get("detail", "Ошибка входа")
        return templates.TemplateResponse(
            name="login.html",
            request=request,
            context={"title": "Вход", "error": error_detail},
            status_code=response.status_code
        )


@router.get("/logout")
async def logout():
    redirect = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    redirect.delete_cookie("access_token")
    return redirect