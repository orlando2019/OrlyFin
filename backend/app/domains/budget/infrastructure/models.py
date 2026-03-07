from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.db.base import Base
from app.shared.infrastructure.db.models.audit_base import AuditBaseMixin


# Modela la responsabilidad de 'budget record' dentro del dominio o capa actual.
class BudgetRecord(Base, AuditBaseMixin):
    __tablename__ = "budget_records"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    period_start: Mapped[date] = mapped_column(Date, index=True)
    period_end: Mapped[date] = mapped_column(Date, index=True)
    planned_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    alert_threshold_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("80.00"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
