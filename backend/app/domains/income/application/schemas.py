from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


# Modela la responsabilidad de 'income create request' dentro del dominio o capa actual.
class IncomeCreateRequest(BaseModel):
    account_id: str | None = None
    category: str = Field(min_length=2, max_length=80)
    description: str = Field(default="", max_length=255)
    amount: Decimal
    income_type: str = Field(default="simple")
    frequency: str | None = Field(default=None, max_length=30)
    occurred_on: date


# Modela la responsabilidad de 'income response' dentro del dominio o capa actual.
class IncomeResponse(BaseModel):
    id: str
    organization_id: str
    account_id: str | None
    category: str
    description: str
    amount: Decimal
    income_type: str
    frequency: str | None
    occurred_on: date


# Modela la responsabilidad de 'income list response' dentro del dominio o capa actual.
class IncomeListResponse(BaseModel):
    incomes: list[IncomeResponse]
