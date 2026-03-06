from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.db.base import Base
from app.shared.infrastructure.db.models.audit_base import AuditBaseMixin


class PaymentRecord(Base, AuditBaseMixin):
    __tablename__ = "payment_records"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), index=True)
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("financial_accounts.id"), index=True)
    payment_type: Mapped[str] = mapped_column(String(20), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    paid_on: Mapped[date] = mapped_column(Date, index=True)
    reference_type: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    reference_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    notes: Mapped[str] = mapped_column(String(255), default="")
