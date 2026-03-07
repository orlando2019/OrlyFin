from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.domains.audit.application.schemas import AuditEventResponse
from app.domains.audit.infrastructure.models import AuditEvent
from app.domains.audit.infrastructure.repository import AuditRepository


# Modela la responsabilidad de 'audit service' dentro del dominio o capa actual.
class AuditService:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuditRepository(db)

    # Ejecuta la lógica principal de 'record event' y devuelve el resultado esperado por el flujo.
    def record_event(
        self,
        organization_id: str | None,
        user_id: str | None,
        module: str,
        action: str,
        entity_type: str | None = None,
        entity_id: str | None = None,
        trace_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> AuditEvent:
        serialized = json.dumps(details or {}, ensure_ascii=True)
        return self.repo.create(
            organization_id=organization_id,
            user_id=user_id,
            module=module,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            trace_id=trace_id,
            details_json=serialized,
        )

    # Lista 'events' según los filtros o el contexto recibido.
    def list_events(self, organization_id: str, module: str | None = None, action: str | None = None, limit: int = 100) -> list[AuditEvent]:
        return self.repo.list_for_org(organization_id=organization_id, module=module, action=action, limit=min(max(limit, 1), 500))



# Transforma la entidad de dominio en la estructura de respuesta 'to audit event response'.
def to_audit_event_response(event: AuditEvent) -> AuditEventResponse:
    details: dict[str, Any]
    try:
        details = json.loads(event.details_json or "{}")
    except json.JSONDecodeError:
        details = {}

    occurred_on = event.occurred_on.isoformat() if isinstance(event.occurred_on, datetime) else str(event.occurred_on)
    return AuditEventResponse(
        id=event.id,
        organization_id=event.organization_id,
        user_id=event.user_id,
        module=event.module,
        action=event.action,
        entity_type=event.entity_type,
        entity_id=event.entity_id,
        trace_id=event.trace_id,
        details=details,
        occurred_on=occurred_on,
    )



# Obtiene 'audit service' y lo expone para su uso en la capa llamadora.
def get_audit_service(db: Session = Depends(get_db)) -> AuditService:
    return AuditService(db)
