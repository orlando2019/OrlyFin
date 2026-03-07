from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.alerts.application.schemas import AlertResponse
from app.domains.alerts.infrastructure.models import AlertRecord
from app.domains.alerts.infrastructure.repository import AlertRepository
from app.domains.audit.application.service import AuditService
from app.domains.budget.infrastructure.models import BudgetRecord
from app.domains.debt.infrastructure.models import DebtRecord
from app.domains.expense.infrastructure.repository import ExpenseRepository


class AlertsService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AlertRepository(db)
        self.audit = AuditService(db)
        self.expense_repo = ExpenseRepository(db)

    def _build_budget_alerts(self, organization_id: str, actor_user_id: str | None) -> int:
        generated = 0
        budgets = self.db.scalars(select(BudgetRecord).where(BudgetRecord.organization_id == organization_id)).all()

        for budget in budgets:
            consumed = self.expense_repo.sum_by_category_period(
                organization_id=organization_id,
                category=budget.category,
                start_on=budget.period_start,
                end_on=budget.period_end,
            )
            planned = Decimal(budget.planned_amount)
            if planned <= 0:
                continue

            usage = (consumed / planned * Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if usage < Decimal(budget.alert_threshold_percent):
                continue

            fingerprint = f"budget-threshold:{budget.id}:{budget.period_end.isoformat()}"
            if self.repo.get_open_by_fingerprint(organization_id, fingerprint):
                continue

            self.repo.create(
                organization_id=organization_id,
                created_by_user_id=actor_user_id,
                module="budget",
                severity="warning",
                channel="internal",
                title="Budget threshold reached",
                message=f"Category {budget.category} reached {usage}% of planned budget.",
                reference_type="budget",
                reference_id=budget.id,
                fingerprint=fingerprint,
            )
            generated += 1

        return generated

    def _build_debt_alerts(self, organization_id: str, actor_user_id: str | None) -> int:
        generated = 0
        due_limit = date.today().toordinal() + settings.alert_debt_due_days

        debts = self.db.scalars(
            select(DebtRecord).where(DebtRecord.organization_id == organization_id, DebtRecord.status == "active")
        ).all()

        for debt in debts:
            if debt.due_on is None:
                continue
            if debt.due_on.toordinal() > due_limit:
                continue

            fingerprint = f"debt-due:{debt.id}:{debt.due_on.isoformat()}"
            if self.repo.get_open_by_fingerprint(organization_id, fingerprint):
                continue

            self.repo.create(
                organization_id=organization_id,
                created_by_user_id=actor_user_id,
                module="debt",
                severity="critical",
                channel="internal",
                title="Debt due soon",
                message=f"Debt with creditor {debt.creditor} is due on {debt.due_on.isoformat()}.",
                reference_type="debt",
                reference_id=debt.id,
                fingerprint=fingerprint,
            )
            generated += 1

        return generated

    def evaluate_alerts(self, organization_id: str, actor_user_id: str, trace_id: str) -> int:
        generated = 0
        generated += self._build_budget_alerts(organization_id, actor_user_id)
        generated += self._build_debt_alerts(organization_id, actor_user_id)

        pending_expenses = self.expense_repo.count_pending(organization_id)
        if pending_expenses >= settings.alert_pending_expense_threshold:
            fingerprint = f"pending-expense-threshold:{date.today().isoformat()}"
            if not self.repo.get_open_by_fingerprint(organization_id, fingerprint):
                self.repo.create(
                    organization_id=organization_id,
                    created_by_user_id=actor_user_id,
                    module="expense",
                    severity="warning",
                    channel="internal",
                    title="Pending expenses threshold",
                    message=f"There are {pending_expenses} pending expenses.",
                    reference_type="expense",
                    reference_id=None,
                    fingerprint=fingerprint,
                )
                generated += 1

        self.audit.record_event(
            organization_id=organization_id,
            user_id=actor_user_id,
            module="alerts",
            action="evaluate",
            entity_type="alert_batch",
            entity_id=None,
            trace_id=trace_id,
            details={"generated": generated},
        )
        self.db.commit()
        return generated

    def list_alerts(self, organization_id: str, status: str | None = None) -> list[AlertRecord]:
        return self.repo.list_for_org(organization_id, status=status)

    def mark_read(self, organization_id: str, alert_id: str, actor_user_id: str, trace_id: str) -> AlertRecord:
        alert = self.repo.get_by_id_for_org(alert_id, organization_id)
        if alert is None:
            raise AppError("NOT_FOUND", "Alert not found", 404)

        if alert.status != "read":
            alert.status = "read"
            alert.read_on = datetime.now(timezone.utc)

        self.audit.record_event(
            organization_id=organization_id,
            user_id=actor_user_id,
            module="alerts",
            action="mark_read",
            entity_type="alert",
            entity_id=alert.id,
            trace_id=trace_id,
            details={"status": alert.status},
        )
        self.db.commit()
        return alert



def to_alert_response(alert: AlertRecord) -> AlertResponse:
    return AlertResponse(
        id=alert.id,
        module=alert.module,
        severity=alert.severity,
        channel=alert.channel,
        title=alert.title,
        message=alert.message,
        reference_type=alert.reference_type,
        reference_id=alert.reference_id,
        status=alert.status,
        triggered_on=alert.triggered_on.isoformat(),
        read_on=alert.read_on.isoformat() if alert.read_on else None,
    )



def get_alerts_service(db: Session = Depends(get_db)) -> AlertsService:
    return AlertsService(db)
