from __future__ import annotations

from decimal import Decimal

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.audit.application.service import AuditService
from app.domains.accounts.infrastructure.repository import AccountRepository
from app.domains.expense.application.schemas import ExpenseCreateRequest, ExpenseResponse
from app.domains.expense.infrastructure.models import ExpenseRecord
from app.domains.expense.infrastructure.repository import ExpenseRepository

ALLOWED_EXPENSE_TYPES = {"simple", "variable", "recurrent"}


class ExpenseService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ExpenseRepository(db)
        self.accounts_repo = AccountRepository(db)
        self.audit = AuditService(db)

    def create_expense(
        self,
        organization_id: str,
        payload: ExpenseCreateRequest,
        actor_user_id: str | None = None,
        trace_id: str | None = None,
    ) -> ExpenseRecord:
        if payload.amount <= 0:
            raise AppError("VALIDATION_ERROR", "amount must be > 0", 400)
        if payload.expense_type not in ALLOWED_EXPENSE_TYPES:
            raise AppError("VALIDATION_ERROR", "Invalid expense_type", 400)

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
            expense_type=payload.expense_type,
            due_on=payload.due_on,
            occurred_on=payload.occurred_on,
            status="pending",
        )
        if actor_user_id:
            self.audit.record_event(
                organization_id=organization_id,
                user_id=actor_user_id,
                module="expense",
                action="create",
                entity_type="expense_record",
                entity_id=record.id,
                trace_id=trace_id,
                details={"amount": str(payload.amount), "category": payload.category, "status": "pending"},
            )
        self.db.commit()
        return record

    def list_expenses(self, organization_id: str) -> list[ExpenseRecord]:
        return self.repo.list_for_org(organization_id)



def to_expense_response(record: ExpenseRecord) -> ExpenseResponse:
    return ExpenseResponse(
        id=record.id,
        organization_id=record.organization_id,
        account_id=record.account_id,
        category=record.category,
        description=record.description,
        amount=Decimal(record.amount),
        expense_type=record.expense_type,
        due_on=record.due_on,
        occurred_on=record.occurred_on,
        status=record.status,
    )



def get_expense_service(db: Session = Depends(get_db)) -> ExpenseService:
    return ExpenseService(db)
