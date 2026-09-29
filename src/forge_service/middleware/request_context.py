import re
from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

import structlog
from fastapi import Request
from starlette.responses import Response
from structlog.contextvars import bind_contextvars, clear_contextvars

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

    bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )

    logger.info("request_started")

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((perf_counter() - started_at) * 1000, 2)

        logger.exception(
            "request_failed",
            duration_ms=duration_ms,
        )
        raise
    else:
        duration_ms = round((perf_counter() - started_at) * 1000, 2)

        response.headers[REQUEST_ID_HEADER] = request_id

        logger.info(
            "request_completed",
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response
    finally:
        clear_contextvars()
