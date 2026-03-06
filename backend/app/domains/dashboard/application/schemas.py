from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class ExecutiveDashboardResponse(BaseModel):
    period_start: date
    period_end: date
    total_income: Decimal
    total_expense: Decimal
    total_payments: Decimal
    outstanding_debt: Decimal
    total_account_balance: Decimal
    total_budget: Decimal
    budget_usage_percent: Decimal
    pending_expenses: int
    active_debts: int
