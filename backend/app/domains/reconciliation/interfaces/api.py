from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_trace_id
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.interfaces.dependencies import require_permission
from app.domains.reconciliation.application.schemas import (
    ReconciliationCreateRequest,
    ReconciliationListResponse,
    ReconciliationResolveRequest,
    ReconciliationResponse,
)
from app.domains.reconciliation.application.service import (
    ReconciliationService,
    get_reconciliation_service,
    to_reconciliation_response,
)

router = APIRouter(prefix="/reconciliations", tags=["reconciliation"])


@router.post("", response_model=ReconciliationResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("reconciliation", "create"))])
def create_reconciliation(
    payload: ReconciliationCreateRequest,
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationResponse:
    record = service.create_reconciliation(
        organization_id=current_user.organization_id,
        actor_user_id=current_user.id,
        trace_id=trace_id,
        payload=payload,
    )
    return to_reconciliation_response(record)


@router.get("", response_model=ReconciliationListResponse, dependencies=[Depends(require_permission("reconciliation", "read"))])
def list_reconciliations(
    account_id: str | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationListResponse:
    rows = service.list_reconciliations(current_user.organization_id, account_id=account_id)
    return ReconciliationListResponse(reconciliations=[to_reconciliation_response(item) for item in rows])


@router.post("/{reconciliation_id}/resolve", response_model=ReconciliationResponse, dependencies=[Depends(require_permission("reconciliation", "update"))])
def resolve_reconciliation(
    reconciliation_id: str,
    payload: ReconciliationResolveRequest,
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconciliationResponse:
    record = service.resolve_reconciliation(
        organization_id=current_user.organization_id,
        actor_user_id=current_user.id,
        trace_id=trace_id,
        reconciliation_id=reconciliation_id,
        notes=payload.notes,
    )
    return to_reconciliation_response(record)
