import os
from datetime import date
from decimal import Decimal
from uuid import uuid4

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///./test_financial_v1.db")
os.environ.setdefault("JWT_ACCESS_SECRET_KEY", "test-access-secret-at-least-32-bytes")
os.environ.setdefault("JWT_REFRESH_SECRET_KEY", "test-refresh-secret-at-least-32-bytes")
os.environ.setdefault("BOOTSTRAP_ADMIN_EMAIL", "admin@orlyfin.local")
os.environ.setdefault("BOOTSTRAP_ADMIN_PASSWORD", "ChangeMe123!")

from fastapi.testclient import TestClient

from app.main import app


def _login(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@orlyfin.local", "password": "ChangeMe123!"},
    )
    assert response.status_code == 200


def test_financial_modules_v1_flow() -> None:
    with TestClient(app) as client:
        _login(client)

        today = date.today().isoformat()
        unique = uuid4().hex[:8]

        account_response = client.post(
            "/api/v1/accounts",
            json={
                "name": f"Main Account {unique}",
                "account_type": "bank",
                "currency_code": "USD",
                "initial_balance": "1000.00",
            },
        )
        assert account_response.status_code == 201
        account_id = account_response.json()["id"]

        income_response = client.post(
            "/api/v1/incomes",
            json={
                "account_id": account_id,
                "category": "salary",
                "description": "Monthly payroll",
                "amount": "500.00",
                "income_type": "simple",
                "occurred_on": today,
            },
        )
        assert income_response.status_code == 201

        expense_response = client.post(
            "/api/v1/expenses",
            json={
                "account_id": account_id,
                "category": "housing",
                "description": "Rent",
                "amount": "300.00",
                "expense_type": "simple",
                "occurred_on": today,
            },
        )
        assert expense_response.status_code == 201
        expense_id = expense_response.json()["id"]

        debt_response = client.post(
            "/api/v1/debts",
            json={
                "account_id": account_id,
                "creditor": "Bank Credit",
                "description": "Personal loan",
                "principal_amount": "1000.00",
                "debt_type": "simple",
                "opened_on": today,
            },
        )
        assert debt_response.status_code == 201
        debt_id = debt_response.json()["id"]

        pay_debt_response = client.post(
            "/api/v1/payments",
            json={
                "account_id": account_id,
                "payment_type": "debt",
                "amount": "200.00",
                "paid_on": today,
                "reference_type": "debt",
                "reference_id": debt_id,
                "notes": "Debt partial payment",
            },
        )
        assert pay_debt_response.status_code == 201

        pay_expense_response = client.post(
            "/api/v1/payments",
            json={
                "account_id": account_id,
                "payment_type": "regular",
                "amount": "300.00",
                "paid_on": today,
                "reference_type": "expense",
                "reference_id": expense_id,
                "notes": "Rent payment",
            },
        )
        assert pay_expense_response.status_code == 201

        budget_response = client.post(
            "/api/v1/budgets",
            json={
                "category": "housing",
                "period_start": today,
                "period_end": today,
                "planned_amount": "600.00",
                "alert_threshold_percent": "80.00",
            },
        )
        assert budget_response.status_code == 201

        accounts_list = client.get("/api/v1/accounts")
        assert accounts_list.status_code == 200
        account_payload = next(item for item in accounts_list.json()["accounts"] if item["id"] == account_id)
        assert Decimal(account_payload["current_balance"]) == Decimal("1000.00")

        expenses_list = client.get("/api/v1/expenses")
        assert expenses_list.status_code == 200
        expense_payload = next(item for item in expenses_list.json()["expenses"] if item["id"] == expense_id)
        assert expense_payload["status"] == "paid"

        debts_list = client.get("/api/v1/debts")
        assert debts_list.status_code == 200
        debt_payload = next(item for item in debts_list.json()["debts"] if item["id"] == debt_id)
        assert Decimal(debt_payload["balance_amount"]) == Decimal("800.00")

        dashboard = client.get("/api/v1/dashboard/executive")
        assert dashboard.status_code == 200
        summary = dashboard.json()
        assert Decimal(summary["total_income"]) >= Decimal("500.00")
        assert Decimal(summary["total_expense"]) >= Decimal("300.00")
        assert Decimal(summary["total_payments"]) >= Decimal("500.00")
        assert Decimal(summary["outstanding_debt"]) >= Decimal("800.00")
