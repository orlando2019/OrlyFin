import os
from uuid import uuid4

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///./test_auth.db")
os.environ.setdefault("JWT_ACCESS_SECRET_KEY", "test-access-secret-at-least-32-bytes")
os.environ.setdefault("JWT_REFRESH_SECRET_KEY", "test-refresh-secret-at-least-32-bytes")
os.environ.setdefault("BOOTSTRAP_ADMIN_EMAIL", "admin@orlyfin.local")
os.environ.setdefault("BOOTSTRAP_ADMIN_PASSWORD", "ChangeMe123!")

from fastapi.testclient import TestClient

from app.main import app


def test_login_and_me() -> None:
    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@orlyfin.local", "password": "ChangeMe123!"},
        )

        assert login_response.status_code == 200
        assert "of_access_token" in login_response.cookies

        me_response = client.get("/api/v1/auth/me")

        assert me_response.status_code == 200
        body = me_response.json()
        assert body["email"] == "admin@orlyfin.local"
        assert "owner_admin" in body["roles"]


def test_create_user_requires_permission_and_creates_user() -> None:
    with TestClient(app) as client:
        unique_email = f"operator-{uuid4().hex[:8]}@orlyfin.local"
        client.post(
            "/api/v1/auth/login",
            json={"email": "admin@orlyfin.local", "password": "ChangeMe123!"},
        )

        response = client.post(
            "/api/v1/users",
            json={
                "email": unique_email,
                "full_name": "Operator One",
                "password": "StrongPass123!",
                "role_names": ["operator"],
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == unique_email
        assert "operator" in data["roles"]
