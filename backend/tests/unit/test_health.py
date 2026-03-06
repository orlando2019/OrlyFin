import os

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///./test_health.db")
os.environ.setdefault("JWT_ACCESS_SECRET_KEY", "test-access-secret-at-least-32-bytes")
os.environ.setdefault("JWT_REFRESH_SECRET_KEY", "test-refresh-secret-at-least-32-bytes")

from fastapi.testclient import TestClient

from app.main import app


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["version"] == "v1"
