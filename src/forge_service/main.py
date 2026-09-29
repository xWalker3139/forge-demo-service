from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from forge_service.api.router import api_router
from forge_service.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.ready = False

    # Future startup operations will be performed here:
    # database checks, telemetry initialization and dependency validation.
    app.state.ready = True

    yield

    # Stop accepting new traffic before shutdown cleanup starts.
    app.state.ready = False


def create_app() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Production-ready reference service for the Forge platform.",
        lifespan=lifespan,
    )

    application.include_router(api_router)

    return application


app = create_app()
