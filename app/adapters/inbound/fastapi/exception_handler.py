from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import DomainError


async def domain_error_handler(request: Request, exc: DomainError):
    """Единый обработчик для всех доменных ошибок."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )
