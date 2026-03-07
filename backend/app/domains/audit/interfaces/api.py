from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.domains.audit.application.schemas import AuditEventListResponse
from app.domains.audit.application.service import AuditService, get_audit_service, to_audit_event_response
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get(
    "/events",
    response_model=AuditEventListResponse,
    dependencies=[Depends(require_permission("audit", "read"))],
)
def list_audit_events(
    module: str | None = Query(default=None),
    action: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
) -> AuditEventListResponse:
    events = service.list_events(current_user.organization_id, module=module, action=action, limit=limit)
    return AuditEventListResponse(events=[to_audit_event_response(item) for item in events])
