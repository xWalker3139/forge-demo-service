import re
from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

import structlog
from fastapi import Request
from starlette.responses import Response
from structlog.contextvars import bind_contextvars, clear_contextvars

from forge_service.core.metrics import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_IN_PROGRESS,
    HTTP_REQUESTS_TOTAL,
)

from forge_service.core.metrics import configure_build_info

METRICS_PATH = "/metrics"
UNMATCHED_ROUTE = "unmatched"

CallNext = Callable[[Request], Awaitable[Response]]

logger = structlog.get_logger()

REQUEST_ID_HEADER = "X-Request-ID"
VALID_REQUEST_ID = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


def resolve_request_id(request: Request) -> str:
    supplied_request_id = request.headers.get(REQUEST_ID_HEADER)

    if supplied_request_id and VALID_REQUEST_ID.fullmatch(supplied_request_id):
        return supplied_request_id

    return str(uuid4())


async def request_context_middleware(
    request: Request,
    call_next: CallNext,
) -> Response:
    clear_contextvars()

    request_id = resolve_request_id(request)
    started_at = perf_counter()
    should_instrument = request.url.path != METRICS_PATH

    bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )

    if should_instrument:
        HTTP_REQUESTS_IN_PROGRESS.labels(method=request.method).inc()

    logger.info("request_started")

    try:
        response = await call_next(request)
    except Exception:
        duration_seconds = perf_counter() - started_at

        if should_instrument:
            record_request_metrics(
                request=request,
                status_code=500,
                duration_seconds=duration_seconds,
            )

        logger.exception(
            "request_failed",
            duration_ms=round(duration_seconds * 1000, 2),
        )
        raise
    else:
        duration_seconds = perf_counter() - started_at

        if should_instrument:
            record_request_metrics(
                request=request,
                status_code=response.status_code,
                duration_seconds=duration_seconds,
            )

        response.headers[REQUEST_ID_HEADER] = request_id

        logger.info(
            "request_completed",
            status_code=response.status_code,
            duration_ms=round(duration_seconds * 1000, 2),
        )

        return response
    finally:
        if should_instrument:
            HTTP_REQUESTS_IN_PROGRESS.labels(method=request.method).dec()

        clear_contextvars()


def resolve_route_template(request: Request) -> str:
    route = request.scope.get("route")
    route_path = getattr(route, "path", None)

    if isinstance(route_path, str):
        return route_path

    return UNMATCHED_ROUTE


def record_request_metrics(
    request: Request,
    status_code: int,
    duration_seconds: float,
) -> None:
    method = request.method
    route = resolve_route_template(request)

    HTTP_REQUESTS_TOTAL.labels(
        method=method,
        route=route,
        status_code=str(status_code),
    ).inc()

    HTTP_REQUEST_DURATION_SECONDS.labels(
        method=method,
        route=route,
    ).observe(duration_seconds)
