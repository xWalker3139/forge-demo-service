import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from forge_service.core.config import Settings, get_settings

router = APIRouter(
    prefix="/internal/simulate",
    tags=["simulation"],
)

SettingsDependency = Annotated[Settings, Depends(get_settings)]

DelayMilliseconds = Annotated[
    int,
    Query(
        ge=0,
        le=5000,
        description="Artificial delay in milliseconds.",
    ),
]

ErrorStatusCode = Annotated[
    int,
    Query(
        ge=400,
        le=599,
        description="HTTP error status to return.",
    ),
]


def ensure_fault_injection_enabled(settings: Settings) -> None:
    if not settings.enable_fault_injection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )


@router.get("/latency")
async def simulate_latency(
    settings: SettingsDependency,
    delay_ms: DelayMilliseconds = 1000,
) -> dict[str, int | str]:
    ensure_fault_injection_enabled(settings)

    await asyncio.sleep(delay_ms / 1000)

    return {
        "status": "completed",
        "delay_ms": delay_ms,
    }


@router.get("/error")
async def simulate_error(
    settings: SettingsDependency,
    status_code: ErrorStatusCode = 500,
) -> None:
    ensure_fault_injection_enabled(settings)

    raise HTTPException(
        status_code=status_code,
        detail="Simulated service failure",
    )
