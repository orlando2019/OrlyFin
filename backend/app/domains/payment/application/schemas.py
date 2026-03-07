from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


# Modela la responsabilidad de 'payment create request' dentro del dominio o capa actual.
class PaymentCreateRequest(BaseModel):
    account_id: str
    payment_type: str = Field(default="regular")
    amount: Decimal
    paid_on: date
    reference_type: str | None = None
    reference_id: str | None = None
    notes: str = Field(default="", max_length=255)


# Modela la responsabilidad de 'payment response' dentro del dominio o capa actual.
class PaymentResponse(BaseModel):
    id: str
    organization_id: str
    account_id: str
    payment_type: str
    amount: Decimal
    paid_on: date
    reference_type: str | None
    reference_id: str | None
    notes: str


# Modela la responsabilidad de 'payment list response' dentro del dominio o capa actual.
class PaymentListResponse(BaseModel):
    payments: list[PaymentResponse]
