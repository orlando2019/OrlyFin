from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.db.base import Base
from app.shared.infrastructure.db.models.audit_base import AuditBaseMixin


# Modela la responsabilidad de 'reconciliation record' dentro del dominio o capa actual.
class ReconciliationRecord(Base, AuditBaseMixin):
    __tablename__ = "reconciliation_records"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), index=True)
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("financial_accounts.id"), index=True)
    period_start: Mapped[date] = mapped_column(Date, index=True)
    period_end: Mapped[date] = mapped_column(Date, index=True)
    book_balance: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    statement_balance: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    difference_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    status: Mapped[str] = mapped_column(String(20), default="unbalanced", index=True)
    notes: Mapped[str] = mapped_column(String(255), default="")
    resolved_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
