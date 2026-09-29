# Forge Demo Service

Production-ready FastAPI reference service deployed and operated through the
Forge Internal Developer Platform.

## Overview

Forge Demo Service demonstrates the application contract required by the Forge
platform. It includes health checks, structured logging, request correlation,
Prometheus metrics, controlled fault injection, configuration management, and
graceful shutdown.

The service is intentionally small. Its purpose is to demonstrate production
operational practices rather than complex business functionality.

## Features

- FastAPI application factory
- Environment-based configuration
- Liveness and readiness health checks
- Structured JSON logging
- Request correlation through `X-Request-ID`
- Prometheus request metrics
- Build information metric
- Controlled latency and error simulation
- Graceful shutdown
- Automated unit tests
- Ruff formatting and linting
- Dependency locking with uv

## Technology Stack

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic Settings
- structlog
- Prometheus Client
- pytest
- Ruff
- uv

## Repository Structure

```text
src/forge_service/
├── api/
│   ├── router.py
│   └── routes/
│       ├── health.py
│       ├── metrics.py
│       └── simulation.py
├── core/
│   ├── config.py
│   ├── logging.py
│   ├── metrics.py
│   └── service_state.py
├── middleware/
│   └── request_context.py
├── __main__.py
└── main.py