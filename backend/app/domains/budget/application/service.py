from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.budget.application.schemas import BudgetCreateRequest, BudgetResponse
from app.domains.budget.infrastructure.models import BudgetRecord
from app.domains.budget.infrastructure.repository import BudgetRepository
from app.domains.expense.infrastructure.repository import ExpenseRepository


class BudgetService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BudgetRepository(db)
        self.expense_repo = ExpenseRepository(db)

    def create_budget(self, organization_id: str, payload: BudgetCreateRequest) -> BudgetRecord:
        if payload.planned_amount <= 0:
            raise AppError("VALIDATION_ERROR", "planned_amount must be > 0", 400)
        if payload.period_end < payload.period_start:
            raise AppError("VALIDATION_ERROR", "period_end must be >= period_start", 400)
        if payload.alert_threshold_percent <= 0 or payload.alert_threshold_percent > 100:
            raise AppError("VALIDATION_ERROR", "alert_threshold_percent must be between 0 and 100", 400)

        record = self.repo.create(
            organization_id=organization_id,
            category=payload.category,
            period_start=payload.period_start,
            period_end=payload.period_end,
            planned_amount=Decimal(payload.planned_amount),
            alert_threshold_percent=Decimal(payload.alert_threshold_percent),
        )
        self.db.commit()
        return record

    def list_budgets(self, organization_id: str) -> list[BudgetRecord]:
        return self.repo.list_for_org(organization_id)

    def to_budget_response(self, organization_id: str, record: BudgetRecord) -> BudgetResponse:
        consumed = self.expense_repo.sum_by_category_period(
            organization_id=organization_id,
            category=record.category,
            start_on=record.period_start,
            end_on=record.period_end,
        )
        planned = Decimal(record.planned_amount)
        usage = Decimal("0.00") if planned == 0 else (consumed / planned * Decimal("100"))
        usage = usage.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return BudgetResponse(
            id=record.id,
            organization_id=record.organization_id,
            category=record.category,
            period_start=record.period_start,
            period_end=record.period_end,
            planned_amount=planned,
            alert_threshold_percent=Decimal(record.alert_threshold_percent),
            consumed_amount=consumed,
            usage_percent=usage,
            threshold_reached=usage >= Decimal(record.alert_threshold_percent),
        )



def get_budget_service(db: Session = Depends(get_db)) -> BudgetService:
    return BudgetService(db)
