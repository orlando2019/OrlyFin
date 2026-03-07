from __future__ import annotations

from pydantic import BaseModel


# Modela la responsabilidad de 'audit event response' dentro del dominio o capa actual.
class AuditEventResponse(BaseModel):
    id: str
    organization_id: str | None
    user_id: str | None
    module: str
    action: str
    entity_type: str | None
    entity_id: str | None
    trace_id: str | None
    details: dict
    occurred_on: str


# Modela la responsabilidad de 'audit event list response' dentro del dominio o capa actual.
class AuditEventListResponse(BaseModel):
    events: list[AuditEventResponse]
