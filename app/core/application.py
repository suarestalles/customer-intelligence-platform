from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="End-to-end Customer Intelligence Platform",
    )

    app.include_router(health_router)

    return app
