from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response, status
from pydantic import BaseModel

from forge_service.core.config import Settings, get_settings

router = APIRouter(tags=["health"])

SettingsDependency = Annotated[Settings, Depends(get_settings)]


class HealthResponse(BaseModel):
    status: str


@router.get(
    "/health/live",
    response_model=HealthResponse,
)
async def liveness() -> HealthResponse:
    return HealthResponse(status="alive")


@router.get(
    "/health/ready",
    response_model=HealthResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "The service is not ready to accept traffic."
        }
    },
)
async def readiness(
    request: Request,
    response: Response,
) -> HealthResponse:
    if not getattr(request.app.state, "ready", False):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(status="not_ready")

    return HealthResponse(status="ready")


@router.get("/version")
async def version(
    settings: SettingsDependency,
) -> dict[str, Any]:
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
