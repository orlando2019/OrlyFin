from __future__ import annotations

from decimal import Decimal

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.audit.application.service import AuditService
from app.domains.accounts.application.schemas import AccountCreateRequest, AccountResponse
from app.domains.accounts.infrastructure.models import FinancialAccount
from app.domains.accounts.infrastructure.repository import AccountRepository

ALLOWED_ACCOUNT_TYPES = {"cash", "bank", "wallet", "credit", "investment", "other"}


class AccountsService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AccountRepository(db)
        self.audit = AuditService(db)

    def create_account(
        self,
        organization_id: str,
        payload: AccountCreateRequest,
        actor_user_id: str | None = None,
        trace_id: str | None = None,
    ) -> FinancialAccount:
        if payload.account_type.lower() not in ALLOWED_ACCOUNT_TYPES:
            raise AppError("VALIDATION_ERROR", "Invalid account_type", 400)
        if payload.initial_balance < 0:
            raise AppError("VALIDATION_ERROR", "initial_balance must be >= 0", 400)

        if self.repo.get_by_name_for_org(payload.name, organization_id):
            raise AppError("CONFLICT", "Account name already exists in organization", 409)

        account = self.repo.create(
            organization_id=organization_id,
            name=payload.name,
            account_type=payload.account_type.lower(),
            currency_code=payload.currency_code.upper(),
            initial_balance=Decimal(payload.initial_balance),
        )
        if actor_user_id:
            self.audit.record_event(
                organization_id=organization_id,
                user_id=actor_user_id,
                module="accounts",
                action="create",
                entity_type="financial_account",
                entity_id=account.id,
                trace_id=trace_id,
                details={"name": account.name, "account_type": account.account_type},
            )
        self.db.commit()
        return account

    def list_accounts(self, organization_id: str) -> list[FinancialAccount]:
        return self.repo.list_for_org(organization_id)



def to_account_response(account: FinancialAccount) -> AccountResponse:
    return AccountResponse(
        id=account.id,
        organization_id=account.organization_id,
        name=account.name,
        account_type=account.account_type,
        currency_code=account.currency_code,
        current_balance=Decimal(account.current_balance),
        is_active=account.is_active,
    )



def get_accounts_service(db: Session = Depends(get_db)) -> AccountsService:
    return AccountsService(db)
