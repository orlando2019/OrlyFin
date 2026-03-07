from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class ReconciliationCreateRequest(BaseModel):
    account_id: str
    period_start: date
    period_end: date
    statement_balance: Decimal
    notes: str = Field(default="", max_length=255)


class ReconciliationResolveRequest(BaseModel):
    notes: str = Field(default="", max_length=255)


class ReconciliationResponse(BaseModel):
    id: str
    account_id: str
    period_start: date
    period_end: date
    book_balance: Decimal
    statement_balance: Decimal
    difference_amount: Decimal
    status: str
    notes: str
    resolved_on: str | None


class ReconciliationListResponse(BaseModel):
    reconciliations: list[ReconciliationResponse]
