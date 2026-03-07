from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


# Modela la responsabilidad de 'budget create request' dentro del dominio o capa actual.
class BudgetCreateRequest(BaseModel):
    category: str = Field(min_length=2, max_length=80)
    period_start: date
    period_end: date
    planned_amount: Decimal
    alert_threshold_percent: Decimal = Field(default=Decimal("80.00"))


# Modela la responsabilidad de 'budget response' dentro del dominio o capa actual.
class BudgetResponse(BaseModel):
    id: str
    organization_id: str
    category: str
    period_start: date
    period_end: date
    planned_amount: Decimal
    alert_threshold_percent: Decimal
    consumed_amount: Decimal
    usage_percent: Decimal
    threshold_reached: bool


# Modela la responsabilidad de 'budget list response' dentro del dominio o capa actual.
class BudgetListResponse(BaseModel):
    budgets: list[BudgetResponse]
