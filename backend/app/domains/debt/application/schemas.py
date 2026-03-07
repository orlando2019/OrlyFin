from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


# Modela la responsabilidad de 'debt create request' dentro del dominio o capa actual.
class DebtCreateRequest(BaseModel):
    account_id: str | None = None
    creditor: str = Field(min_length=2, max_length=120)
    description: str = Field(default="", max_length=255)
    principal_amount: Decimal
    debt_type: str = Field(default="simple")
    total_installments: int | None = None
    opened_on: date
    due_on: date | None = None


# Modela la responsabilidad de 'debt response' dentro del dominio o capa actual.
class DebtResponse(BaseModel):
    id: str
    organization_id: str
    account_id: str | None
    creditor: str
    description: str
    principal_amount: Decimal
    balance_amount: Decimal
    debt_type: str
    total_installments: int | None
    paid_installments: int
    opened_on: date
    due_on: date | None
    status: str


# Modela la responsabilidad de 'debt list response' dentro del dominio o capa actual.
class DebtListResponse(BaseModel):
    debts: list[DebtResponse]
