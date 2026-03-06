from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domains.income.infrastructure.models import IncomeRecord


class IncomeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        organization_id: str,
        account_id: str | None,
        category: str,
        description: str,
        amount: Decimal,
        income_type: str,
        frequency: str | None,
        occurred_on: date,
    ) -> IncomeRecord:
        record = IncomeRecord(
            organization_id=organization_id,
            account_id=account_id,
            category=category,
            description=description,
            amount=amount,
            income_type=income_type,
            frequency=frequency,
            occurred_on=occurred_on,
        )
        self.db.add(record)
        self.db.flush()
        return record

    def list_for_org(self, organization_id: str) -> list[IncomeRecord]:
        rows = self.db.scalars(
            select(IncomeRecord)
            .where(IncomeRecord.organization_id == organization_id)
            .order_by(IncomeRecord.occurred_on.desc(), IncomeRecord.created_at.desc())
        ).all()
        return list(rows)

    def sum_for_period(self, organization_id: str, start_on: date, end_on: date) -> Decimal:
        total = self.db.scalar(
            select(func.coalesce(func.sum(IncomeRecord.amount), 0)).where(
                IncomeRecord.organization_id == organization_id,
                IncomeRecord.occurred_on >= start_on,
                IncomeRecord.occurred_on <= end_on,
            )
        )
        return Decimal(total or 0)
