from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


# Modela la responsabilidad de 'expense create request' dentro del dominio o capa actual.
class ExpenseCreateRequest(BaseModel):
    account_id: str | None = None
    category: str = Field(min_length=2, max_length=80)
    description: str = Field(default="", max_length=255)
    amount: Decimal
    expense_type: str = Field(default="simple")
    due_on: date | None = None
    occurred_on: date


# Modela la responsabilidad de 'expense response' dentro del dominio o capa actual.
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


# Modela la responsabilidad de 'expense list response' dentro del dominio o capa actual.
class ExpenseListResponse(BaseModel):
    expenses: list[ExpenseResponse]
