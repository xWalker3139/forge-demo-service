from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from forge_service.core.config import Settings, get_settings
from forge_service.main import app


@pytest.fixture
def fault_injection_client() -> Iterator[TestClient]:
    app.dependency_overrides[get_settings] = lambda: Settings(enable_fault_injection=True)

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_fault_injection_is_disabled_by_default() -> None:
    with TestClient(app) as client:
        response = client.get("/internal/simulate/latency?delay_ms=1")

    assert response.status_code == 404


def test_simulated_latency(
    fault_injection_client: TestClient,
) -> None:
    response = fault_injection_client.get("/internal/simulate/latency?delay_ms=1")

    assert response.status_code == 200
    assert response.json() == {
        "status": "completed",
        "delay_ms": 1,
    }


def test_simulated_error(
    fault_injection_client: TestClient,
) -> None:
    response = fault_injection_client.get("/internal/simulate/error?status_code=503")

    assert response.status_code == 503
    assert response.json() == {"detail": "Simulated service failure"}


def test_latency_validation(
    fault_injection_client: TestClient,
) -> None:
    response = fault_injection_client.get("/internal/simulate/latency?delay_ms=6000")

    assert response.status_code == 422


def test_error_status_validation(
    fault_injection_client: TestClient,
) -> None:
    response = fault_injection_client.get("/internal/simulate/error?status_code=200")

    assert response.status_code == 422
