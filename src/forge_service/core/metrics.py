from prometheus_client import Counter, Gauge, Histogram, Info

HTTP_REQUESTS_TOTAL = Counter(
    "forge_http_requests_total",
    "Total number of HTTP requests.",
    ["method", "route", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "forge_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "route"],
    buckets=(
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
        10.0,
    ),
)

HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "forge_http_requests_in_progress",
    "Number of HTTP requests currently being processed.",
    ["method"],
)

BUILD_INFO = Info(
    "forge_build",
    "Forge Demo Service build information.",
)


def configure_build_info(
    version: str,
    environment: str,
) -> None:
    BUILD_INFO.info(
        {
            "version": version,
            "environment": environment,
        }
    )
