from fastapi.testclient import TestClient

from forge_service.main import app


def test_liveness_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_version_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Forge Demo Service",
        "version": "0.1.0",
        "environment": "local",
    }


def test_response_contains_request_id() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


def test_valid_request_id_is_propagated() -> None:
    request_id = "integration-test-123"

    with TestClient(app) as client:
        response = client.get(
            "/health/live",
            headers={"X-Request-ID": request_id},
        )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id


def test_invalid_request_id_is_replaced() -> None:
    invalid_request_id = "invalid request id"

    with TestClient(app) as client:
        response = client.get(
            "/health/live",
            headers={"X-Request-ID": invalid_request_id},
        )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] != invalid_request_id
