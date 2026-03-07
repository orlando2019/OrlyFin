from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.accounts.infrastructure.repository import AccountRepository
from app.domains.audit.application.service import AuditService
from app.domains.reconciliation.application.schemas import (
    ReconciliationCreateRequest,
    ReconciliationResponse,
)
from app.domains.reconciliation.infrastructure.models import ReconciliationRecord
from app.domains.reconciliation.infrastructure.repository import ReconciliationRepository


class ReconciliationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReconciliationRepository(db)
        self.accounts_repo = AccountRepository(db)
        self.audit = AuditService(db)

    def create_reconciliation(
        self,
        organization_id: str,
        actor_user_id: str,
        trace_id: str,
        payload: ReconciliationCreateRequest,
    ) -> ReconciliationRecord:
        if payload.period_end < payload.period_start:
            raise AppError("VALIDATION_ERROR", "period_end must be >= period_start", 400)

        account = self.accounts_repo.get_by_id_for_org(payload.account_id, organization_id)
        if account is None:
            raise AppError("NOT_FOUND", "Account not found", 404)

        book_balance = Decimal(account.current_balance)
        statement_balance = Decimal(payload.statement_balance)
        difference = statement_balance - book_balance
        status = "balanced" if difference == 0 else "unbalanced"

        record = self.repo.create(
            organization_id=organization_id,
            account_id=payload.account_id,
            period_start=payload.period_start,
            period_end=payload.period_end,
            book_balance=book_balance,
            statement_balance=statement_balance,
            difference_amount=difference,
            status=status,
            notes=payload.notes,
        )

        self.audit.record_event(
            organization_id=organization_id,
            user_id=actor_user_id,
            module="reconciliation",
            action="create",
            entity_type="reconciliation",
            entity_id=record.id,
            trace_id=trace_id,
            details={"account_id": payload.account_id, "difference_amount": str(difference), "status": status},
        )

        self.db.commit()
        return record

    def resolve_reconciliation(
        self,
        organization_id: str,
        actor_user_id: str,
        trace_id: str,
        reconciliation_id: str,
        notes: str,
    ) -> ReconciliationRecord:
        record = self.repo.get_by_id_for_org(reconciliation_id, organization_id)
        if record is None:
            raise AppError("NOT_FOUND", "Reconciliation not found", 404)

        record.status = "resolved"
        record.notes = notes or record.notes
        record.resolved_on = datetime.now(timezone.utc)

        self.audit.record_event(
            organization_id=organization_id,
            user_id=actor_user_id,
            module="reconciliation",
            action="resolve",
            entity_type="reconciliation",
            entity_id=record.id,
            trace_id=trace_id,
            details={"status": record.status},
        )
        self.db.commit()
        return record

    def list_reconciliations(self, organization_id: str, account_id: str | None = None) -> list[ReconciliationRecord]:
        return self.repo.list_for_org(organization_id, account_id=account_id)



def to_reconciliation_response(record: ReconciliationRecord) -> ReconciliationResponse:
    return ReconciliationResponse(
        id=record.id,
        account_id=record.account_id,
        period_start=record.period_start,
        period_end=record.period_end,
        book_balance=Decimal(record.book_balance),
        statement_balance=Decimal(record.statement_balance),
        difference_amount=Decimal(record.difference_amount),
        status=record.status,
        notes=record.notes,
        resolved_on=record.resolved_on.isoformat() if record.resolved_on else None,
    )



def get_reconciliation_service(db: Session = Depends(get_db)) -> ReconciliationService:
    return ReconciliationService(db)
