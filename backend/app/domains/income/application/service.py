from __future__ import annotations

from decimal import Decimal

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.audit.application.service import AuditService
from app.domains.accounts.infrastructure.repository import AccountRepository
from app.domains.income.application.schemas import IncomeCreateRequest, IncomeResponse
from app.domains.income.infrastructure.models import IncomeRecord
from app.domains.income.infrastructure.repository import IncomeRepository

ALLOWED_INCOME_TYPES = {"simple", "variable", "recurrent"}


class IncomeService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = IncomeRepository(db)
        self.accounts_repo = AccountRepository(db)
        self.audit = AuditService(db)

    def create_income(
        self,
        organization_id: str,
        payload: IncomeCreateRequest,
        actor_user_id: str | None = None,
        trace_id: str | None = None,
    ) -> IncomeRecord:
        if payload.amount <= 0:
            raise AppError("VALIDATION_ERROR", "amount must be > 0", 400)
        if payload.income_type not in ALLOWED_INCOME_TYPES:
            raise AppError("VALIDATION_ERROR", "Invalid income_type", 400)

        account = None
        if payload.account_id:
            account = self.accounts_repo.get_by_id_for_org(payload.account_id, organization_id)
            if account is None:
                raise AppError("NOT_FOUND", "Account not found", 404)

        record = self.repo.create(
            organization_id=organization_id,
            account_id=payload.account_id,
            category=payload.category,
            description=payload.description,
            amount=Decimal(payload.amount),
            income_type=payload.income_type,
            frequency=payload.frequency,
            occurred_on=payload.occurred_on,
        )

        if account is not None:
            account.current_balance = Decimal(account.current_balance) + Decimal(payload.amount)

        if actor_user_id:
            self.audit.record_event(
                organization_id=organization_id,
                user_id=actor_user_id,
                module="income",
                action="create",
                entity_type="income_record",
                entity_id=record.id,
                trace_id=trace_id,
                details={"amount": str(payload.amount), "category": payload.category, "income_type": payload.income_type},
            )

        self.db.commit()
        return record

    def list_incomes(self, organization_id: str) -> list[IncomeRecord]:
        return self.repo.list_for_org(organization_id)



def to_income_response(record: IncomeRecord) -> IncomeResponse:
    return IncomeResponse(
        id=record.id,
        organization_id=record.organization_id,
        account_id=record.account_id,
        category=record.category,
        description=record.description,
        amount=Decimal(record.amount),
        income_type=record.income_type,
        frequency=record.frequency,
        occurred_on=record.occurred_on,
    )



def get_income_service(db: Session = Depends(get_db)) -> IncomeService:
    return IncomeService(db)
