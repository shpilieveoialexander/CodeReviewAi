import multiprocessing

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from api.v1.api import router_v1
from core.settings import settings

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=f"{settings.PROJECT_NAME}",
    version=settings.VERSION,
    openapi_url=f"/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router_v1, prefix=f"/api/v1")


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )


max_workers_count = multiprocessing.cpu_count() * 2 + 1

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        log_level="info",
        reload=True,
        workers=max_workers_count,
    )
