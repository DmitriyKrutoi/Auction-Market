from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config.config import settings
from app.adapters.inbound.fastapi.routes import auth, users
from app.adapters.inbound.web.routes import auth as web_auth, pages as web_pages

app = FastAPI(title=settings.app_name, debug=settings.debug)

# Подключаем статику
app.mount("/static", StaticFiles(directory="app/adapters/inbound/web/static"), name="static")

# Подключаем шаблоны
templates = Jinja2Templates(directory="app/adapters/inbound/web/templates")

# API роуты
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

# Web роуты
app.include_router(web_auth.router)
app.include_router(web_pages.router)