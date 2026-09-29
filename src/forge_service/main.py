from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from forge_service.api.router import api_router
from forge_service.core.config import get_settings

from forge_service.core.metrics import configure_build_info
import structlog

from forge_service.core.logging import configure_logging
from forge_service.middleware.request_context import request_context_middleware

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()

    app.state.ready = False

    logger.info(
        "application_starting",
        app_name=settings.app_name,
        app_version=settings.app_version,
        environment=settings.environment,
    )

    app.state.ready = True

    logger.info("application_ready")

    yield

    app.state.ready = False

    logger.info("application_stopped")


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    configure_build_info(
        version=settings.app_version,
        environment=settings.environment,
    )

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Production-ready reference service for the Forge platform.",
        lifespan=lifespan,
    )

    application.middleware("http")(request_context_middleware)
    application.include_router(api_router)

    return application


app = create_app()
