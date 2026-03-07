from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.db.base import Base
from app.shared.infrastructure.db.models.audit_base import AuditBaseMixin


# Modela la responsabilidad de 'audit event' dentro del dominio o capa actual.
class AuditEvent(Base, AuditBaseMixin):
    __tablename__ = "audit_events"

    organization_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("organizations.id"), index=True, nullable=True)
    user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), index=True, nullable=True)
    module: Mapped[str] = mapped_column(String(80), index=True)
    action: Mapped[str] = mapped_column(String(40), index=True)
    entity_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    trace_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    details_json: Mapped[str] = mapped_column(Text, default="{}")
    occurred_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
