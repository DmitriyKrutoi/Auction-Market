from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.adapters.inbound.fastapi.routes import auth, events, markets, users
from app.adapters.inbound.web.routes import auth as web_auth
from app.adapters.inbound.web.routes import pages as web_pages
from app.config.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

# Подключаем статику
app.mount(
    "/static", StaticFiles(directory="app/adapters/inbound/web/static"), name="static"
)
app = FastAPI(title=settings.app_name, debug=settings.debug)

# Подключаем шаблоны
templates = Jinja2Templates(directory="app/adapters/inbound/web/templates")

# API роуты
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(markets.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
# Web роуты
app.include_router(web_auth.router)
app.include_router(web_pages.router)
