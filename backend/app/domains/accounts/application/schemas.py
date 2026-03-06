from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field


class AccountCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    account_type: str = Field(min_length=2, max_length=40)
    currency_code: str = Field(min_length=3, max_length=3)
    initial_balance: Decimal = Field(default=Decimal("0.00"))


class AccountResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    account_type: str
    currency_code: str
    current_balance: Decimal
    is_active: bool


class AccountListResponse(BaseModel):
    accounts: list[AccountResponse]
