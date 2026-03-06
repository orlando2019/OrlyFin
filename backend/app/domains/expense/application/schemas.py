from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class ExpenseCreateRequest(BaseModel):
    account_id: str | None = None
    category: str = Field(min_length=2, max_length=80)
    description: str = Field(default="", max_length=255)
    amount: Decimal
    expense_type: str = Field(default="simple")
    due_on: date | None = None
    occurred_on: date


class ExpenseResponse(BaseModel):
    id: str
    organization_id: str
    account_id: str | None
    category: str
    description: str
    amount: Decimal
    expense_type: str
    due_on: date | None
    occurred_on: date
    status: str


class ExpenseListResponse(BaseModel):
    expenses: list[ExpenseResponse]
