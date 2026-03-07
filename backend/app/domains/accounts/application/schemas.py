from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field


# Modela la responsabilidad de 'account create request' dentro del dominio o capa actual.
class AccountCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    account_type: str = Field(min_length=2, max_length=40)
    currency_code: str = Field(min_length=3, max_length=3)
    initial_balance: Decimal = Field(default=Decimal("0.00"))


# Modela la responsabilidad de 'account response' dentro del dominio o capa actual.
class AccountResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    account_type: str
    currency_code: str
    current_balance: Decimal
    is_active: bool


# Modela la responsabilidad de 'account list response' dentro del dominio o capa actual.
class AccountListResponse(BaseModel):
    accounts: list[AccountResponse]
