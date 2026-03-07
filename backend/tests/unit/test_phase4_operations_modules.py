import os
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///./test_phase4_ops.db")
os.environ.setdefault("JWT_ACCESS_SECRET_KEY", "test-access-secret-at-least-32-bytes")
os.environ.setdefault("JWT_REFRESH_SECRET_KEY", "test-refresh-secret-at-least-32-bytes")
os.environ.setdefault("BOOTSTRAP_ADMIN_EMAIL", "admin@orlyfin.local")
os.environ.setdefault("BOOTSTRAP_ADMIN_PASSWORD", "ChangeMe123!")
os.environ.setdefault("ATTACHMENTS_STORAGE_PATH", "./storage/test-attachments")
os.environ.setdefault("ATTACHMENT_MAX_SIZE_MB", "2")
os.environ.setdefault("ATTACHMENT_ALLOWED_MIME_TYPES", "text/plain,application/pdf")
os.environ.setdefault("ALERT_DEBT_DUE_DAYS", "7")
os.environ.setdefault("ALERT_PENDING_EXPENSE_THRESHOLD", "10")

from fastapi.testclient import TestClient

from app.main import app


def _login(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@orlyfin.local", "password": "ChangeMe123!"},
    )
    assert response.status_code == 200


def test_phase4_modules_flow() -> None:
    with TestClient(app) as client:
        _login(client)

        today = date.today()
        unique = uuid4().hex[:8]

        account_response = client.post(
            "/api/v1/accounts",
            json={
                "name": f"Ops Account {unique}",
                "account_type": "bank",
                "currency_code": "USD",
                "initial_balance": "1000.00",
            },
        )
        assert account_response.status_code == 201
        account_id = account_response.json()["id"]

        expense_response = client.post(
            "/api/v1/expenses",
            json={
                "account_id": account_id,
                "category": "housing",
                "description": "Phase4 expense",
                "amount": "120.00",
                "expense_type": "simple",
                "occurred_on": today.isoformat(),
            },
        )
        assert expense_response.status_code == 201
        expense_id = expense_response.json()["id"]

        budget_response = client.post(
            "/api/v1/budgets",
            json={
                "category": "housing",
                "period_start": today.isoformat(),
                "period_end": today.isoformat(),
                "planned_amount": "150.00",
                "alert_threshold_percent": "70.00",
            },
        )
        assert budget_response.status_code == 201

        debt_response = client.post(
            "/api/v1/debts",
            json={
                "account_id": account_id,
                "creditor": "Ops Bank",
                "description": "Ops debt",
                "principal_amount": "500.00",
                "debt_type": "simple",
                "opened_on": today.isoformat(),
                "due_on": (today + timedelta(days=2)).isoformat(),
            },
        )
        assert debt_response.status_code == 201

        evaluate_response = client.post("/api/v1/alerts/evaluate")
        assert evaluate_response.status_code == 200
        assert evaluate_response.json()["generated"] >= 1

        alerts_response = client.get("/api/v1/alerts")
        assert alerts_response.status_code == 200
        alerts = alerts_response.json()["alerts"]
        assert len(alerts) >= 1
        alert_id = alerts[0]["id"]

        read_response = client.post(f"/api/v1/alerts/{alert_id}/read")
        assert read_response.status_code == 200
        assert read_response.json()["status"] == "read"

        setting_response = client.post(
            "/api/v1/settings",
            json={"key": "reporting.default_currency", "value": "USD", "value_type": "string", "is_sensitive": False},
        )
        assert setting_response.status_code == 200

        setting_get = client.get("/api/v1/settings/reporting.default_currency")
        assert setting_get.status_code == 200
        assert setting_get.json()["value"] == "USD"

        attachment_upload = client.post(
            "/api/v1/attachments/upload",
            data={"module": "expense", "entity_id": expense_id},
            files={"file": ("receipt.txt", b"phase4 attachment content", "text/plain")},
        )
        assert attachment_upload.status_code == 200
        attachment_id = attachment_upload.json()["id"]

        attachments_list = client.get(f"/api/v1/attachments?module=expense&entity_id={expense_id}")
        assert attachments_list.status_code == 200
        assert any(item["id"] == attachment_id for item in attachments_list.json()["attachments"])

        attachment_delete = client.delete(f"/api/v1/attachments/{attachment_id}")
        assert attachment_delete.status_code == 200
        assert attachment_delete.json()["status"] == "deleted"

        reconciliation_create = client.post(
            "/api/v1/reconciliations",
            json={
                "account_id": account_id,
                "period_start": today.isoformat(),
                "period_end": today.isoformat(),
                "statement_balance": "950.00",
                "notes": "bank statement loaded",
            },
        )
        assert reconciliation_create.status_code == 201
        reconciliation_id = reconciliation_create.json()["id"]

        reconciliation_resolve = client.post(
            f"/api/v1/reconciliations/{reconciliation_id}/resolve",
            json={"notes": "difference explained"},
        )
        assert reconciliation_resolve.status_code == 200
        assert reconciliation_resolve.json()["status"] == "resolved"

        audit_events = client.get("/api/v1/audit/events?limit=50")
        assert audit_events.status_code == 200
        events = audit_events.json()["events"]
        assert len(events) >= 3
        assert any(event["module"] == "attachments" for event in events)
        assert any(event["module"] == "reconciliation" for event in events)
        assert any(event["module"] == "settings" for event in events)

        dashboard = client.get("/api/v1/dashboard/executive")
        assert dashboard.status_code == 200
        summary = dashboard.json()
        assert Decimal(summary["total_expense"]) >= Decimal("120.00")
