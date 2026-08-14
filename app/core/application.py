import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from app.api.routes.analytics_routes import router as analytics_router
from app.api.routes.health_routes import router as health_router
from app.core.config import settings
from app.core.exceptions_handle import unhandled_exception_handler
from app.core.logging import setup_logging
from app.core.middleware import request_logging_middleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    setup_logging()

    logger.info(
        "Application starting | environment=%s | version=%s",
        settings.environment,
        settings.version,
    )

    yield

    logger.info("Application shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="End-to-end Customer Intelligence Platform",
        lifespan=lifespan,
    )

    app.middleware("http")(request_logging_middleware)

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )

    app.include_router(health_router)
    app.include_router(analytics_router)

    return app
