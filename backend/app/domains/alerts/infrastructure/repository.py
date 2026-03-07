from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.alerts.infrastructure.models import AlertRecord


class AlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_open_by_fingerprint(self, organization_id: str, fingerprint: str) -> AlertRecord | None:
        return self.db.scalar(
            select(AlertRecord).where(
                AlertRecord.organization_id == organization_id,
                AlertRecord.fingerprint == fingerprint,
                AlertRecord.status.in_(["unread", "read"]),
            )
        )

    def create(
        self,
        organization_id: str,
        created_by_user_id: str | None,
        module: str,
        severity: str,
        channel: str,
        title: str,
        message: str,
        reference_type: str | None,
        reference_id: str | None,
        fingerprint: str,
    ) -> AlertRecord:
        alert = AlertRecord(
            organization_id=organization_id,
            created_by_user_id=created_by_user_id,
            module=module,
            severity=severity,
            channel=channel,
            title=title,
            message=message,
            reference_type=reference_type,
            reference_id=reference_id,
            fingerprint=fingerprint,
            status="unread",
        )
        self.db.add(alert)
        self.db.flush()
        return alert

    def get_by_id_for_org(self, alert_id: str, organization_id: str) -> AlertRecord | None:
        return self.db.scalar(select(AlertRecord).where(AlertRecord.id == alert_id, AlertRecord.organization_id == organization_id))

    def list_for_org(self, organization_id: str, status: str | None = None) -> list[AlertRecord]:
        query = select(AlertRecord).where(AlertRecord.organization_id == organization_id)
        if status:
            query = query.where(AlertRecord.status == status)
        rows = self.db.scalars(query.order_by(AlertRecord.triggered_on.desc(), AlertRecord.created_at.desc())).all()
        return list(rows)
