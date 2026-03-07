from __future__ import annotations

from pydantic import BaseModel


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


class AuditEventListResponse(BaseModel):
    events: list[AuditEventResponse]
