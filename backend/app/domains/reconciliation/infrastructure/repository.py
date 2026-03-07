from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.reconciliation.infrastructure.models import ReconciliationRecord


class ReconciliationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        organization_id: str,
        account_id: str,
        period_start: date,
        period_end: date,
        book_balance: Decimal,
        statement_balance: Decimal,
        difference_amount: Decimal,
        status: str,
        notes: str,
    ) -> ReconciliationRecord:
        record = ReconciliationRecord(
            organization_id=organization_id,
            account_id=account_id,
            period_start=period_start,
            period_end=period_end,
            book_balance=book_balance,
            statement_balance=statement_balance,
            difference_amount=difference_amount,
            status=status,
            notes=notes,
        )
        self.db.add(record)
        self.db.flush()
        return record

    def get_by_id_for_org(self, reconciliation_id: str, organization_id: str) -> ReconciliationRecord | None:
        return self.db.scalar(
            select(ReconciliationRecord).where(
                ReconciliationRecord.id == reconciliation_id,
                ReconciliationRecord.organization_id == organization_id,
            )
        )

    def list_for_org(self, organization_id: str, account_id: str | None = None) -> list[ReconciliationRecord]:
        query = select(ReconciliationRecord).where(ReconciliationRecord.organization_id == organization_id)
        if account_id:
            query = query.where(ReconciliationRecord.account_id == account_id)

        rows = self.db.scalars(
            query.order_by(ReconciliationRecord.period_end.desc(), ReconciliationRecord.created_at.desc())
        ).all()
        return list(rows)
