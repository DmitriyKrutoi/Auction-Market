from fastapi import FastAPI
from app.config.config import settings
from contextlib import asynccontextmanager
from app.adapters.inbound.fastapi.routes import auth, users
from app.adapters.outbound.persistence.models import Base
from app.adapters.inbound.fastapi.dependencies import engine

app = FastAPI(title=settings.app_name)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}