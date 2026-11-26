
from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_system_status_endpoint():
    response = client.get("/api/v1/status")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "ORBITAL"
    assert data["version"] == "1.0.0"
    assert data["status"] == "operational"
    assert data["visualization_mode"] == "simulation"


def test_system_status_timestamp():
    response = client.get("/api/v1/status")

    assert response.status_code == 200

    timestamp = datetime.fromisoformat(
        response.json()["timestamp"].replace("Z", "+00:00")
    )

    assert timestamp.tzinfo is not None


def test_dashboard_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "ORBITAL" in response.text


def test_invalid_endpoint():
    response = client.get("/api/v1/nonexistent")

    assert response.status_code == 404
