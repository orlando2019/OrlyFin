from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.db.base import Base
from app.shared.infrastructure.db.models.audit_base import AuditBaseMixin


# Modela la responsabilidad de 'debt record' dentro del dominio o capa actual.
class DebtRecord(Base, AuditBaseMixin):
    __tablename__ = "debt_records"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), index=True)
    account_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("financial_accounts.id"), index=True, nullable=True)
    creditor: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str] = mapped_column(String(255), default="")
    principal_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    balance_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), index=True)
    debt_type: Mapped[str] = mapped_column(String(20), index=True)
    total_installments: Mapped[int | None] = mapped_column(Integer, nullable=True)
    paid_installments: Mapped[int] = mapped_column(Integer, default=0)
    opened_on: Mapped[date] = mapped_column(Date, index=True)
    due_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)
