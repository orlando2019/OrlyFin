from __future__ import annotations

from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.domains.accounts.infrastructure.repository import AccountRepository
from app.domains.budget.infrastructure.repository import BudgetRepository
from app.domains.dashboard.application.schemas import ExecutiveDashboardResponse
from app.domains.debt.infrastructure.repository import DebtRepository
from app.domains.expense.infrastructure.repository import ExpenseRepository
from app.domains.income.infrastructure.repository import IncomeRepository
from app.domains.payment.infrastructure.repository import PaymentRepository


class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.income_repo = IncomeRepository(db)
        self.expense_repo = ExpenseRepository(db)
        self.debt_repo = DebtRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.budget_repo = BudgetRepository(db)
        self.account_repo = AccountRepository(db)

    def get_executive_summary(self, organization_id: str, reference_date: date | None = None) -> ExecutiveDashboardResponse:
        ref = reference_date or date.today()
        period_start = ref.replace(day=1)
        period_end = ref

        total_income = self.income_repo.sum_for_period(organization_id, period_start, period_end)
        total_expense = self.expense_repo.sum_for_period(organization_id, period_start, period_end)
        total_payments = self.payment_repo.sum_for_period(organization_id, period_start, period_end)
        outstanding_debt = self.debt_repo.sum_outstanding(organization_id)
        total_account_balance = self.account_repo.sum_balances_for_org(organization_id)
        total_budget = self.budget_repo.sum_planned_for_overlap(organization_id, period_start, period_end)

        budget_usage = Decimal("0.00") if total_budget == 0 else (total_expense / total_budget * Decimal("100"))
        budget_usage = budget_usage.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return ExecutiveDashboardResponse(
            period_start=period_start,
            period_end=period_end,
            total_income=total_income,
            total_expense=total_expense,
            total_payments=total_payments,
            outstanding_debt=outstanding_debt,
            total_account_balance=total_account_balance,
            total_budget=total_budget,
            budget_usage_percent=budget_usage,
            pending_expenses=self.expense_repo.count_pending(organization_id),
            active_debts=self.debt_repo.count_active(organization_id),
        )



def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(db)
