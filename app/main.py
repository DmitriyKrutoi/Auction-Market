from fastapi import FastAPI
from app.config.config import settings
from app.adapters.inbound.fastapi.routes import auth, users


app = FastAPI(title=settings.app_name)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}