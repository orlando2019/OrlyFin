from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.audit.infrastructure.models import AuditEvent


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        organization_id: str | None,
        user_id: str | None,
        module: str,
        action: str,
        entity_type: str | None,
        entity_id: str | None,
        trace_id: str | None,
        details_json: str,
    ) -> AuditEvent:
        event = AuditEvent(
            organization_id=organization_id,
            user_id=user_id,
            module=module,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            trace_id=trace_id,
            details_json=details_json,
        )
        self.db.add(event)
        self.db.flush()
        return event

    def list_for_org(
        self,
        organization_id: str,
        module: str | None = None,
        action: str | None = None,
        limit: int = 100,
    ) -> list[AuditEvent]:
        query = select(AuditEvent).where(AuditEvent.organization_id == organization_id)
        if module:
            query = query.where(AuditEvent.module == module)
        if action:
            query = query.where(AuditEvent.action == action)

        rows = self.db.scalars(query.order_by(AuditEvent.occurred_on.desc()).limit(limit)).all()
        return list(rows)
