from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.db.base import Base
from app.shared.infrastructure.db.models.audit_base import AuditBaseMixin


# Modela la responsabilidad de 'income record' dentro del dominio o capa actual.
class IncomeRecord(Base, AuditBaseMixin):
    __tablename__ = "income_records"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), index=True)
    account_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("financial_accounts.id"), index=True, nullable=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str] = mapped_column(String(255), default="")
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    income_type: Mapped[str] = mapped_column(String(30), index=True)
    frequency: Mapped[str | None] = mapped_column(String(30), nullable=True)
    occurred_on: Mapped[date] = mapped_column(Date, index=True)
