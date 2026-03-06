from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domains.payment.infrastructure.models import PaymentRecord


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        organization_id: str,
        account_id: str,
        payment_type: str,
        amount: Decimal,
        paid_on: date,
        reference_type: str | None,
        reference_id: str | None,
        notes: str,
    ) -> PaymentRecord:
        record = PaymentRecord(
            organization_id=organization_id,
            account_id=account_id,
            payment_type=payment_type,
            amount=amount,
            paid_on=paid_on,
            reference_type=reference_type,
            reference_id=reference_id,
            notes=notes,
        )
        self.db.add(record)
        self.db.flush()
        return record

    def list_for_org(self, organization_id: str) -> list[PaymentRecord]:
        rows = self.db.scalars(
            select(PaymentRecord)
            .where(PaymentRecord.organization_id == organization_id)
            .order_by(PaymentRecord.paid_on.desc(), PaymentRecord.created_at.desc())
        ).all()
        return list(rows)

    def sum_for_period(self, organization_id: str, start_on: date, end_on: date) -> Decimal:
        total = self.db.scalar(
            select(func.coalesce(func.sum(PaymentRecord.amount), 0)).where(
                PaymentRecord.organization_id == organization_id,
                PaymentRecord.paid_on >= start_on,
                PaymentRecord.paid_on <= end_on,
            )
        )
        return Decimal(total or 0)
