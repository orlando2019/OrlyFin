from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.debt.application.schemas import DebtCreateRequest, DebtListResponse
from app.domains.debt.application.service import DebtService, get_debt_service, to_debt_response
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/debts", tags=["debt"])


@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("debt", "create"))])
def create_debt(
    payload: DebtCreateRequest,
    current_user: User = Depends(get_current_user),
    service: DebtService = Depends(get_debt_service),
):
    record = service.create_debt(current_user.organization_id, payload)
    return to_debt_response(record)


@router.get("", response_model=DebtListResponse, dependencies=[Depends(require_permission("debt", "read"))])
def list_debts(
    current_user: User = Depends(get_current_user),
    service: DebtService = Depends(get_debt_service),
) -> DebtListResponse:
    items = service.list_debts(current_user.organization_id)
    return DebtListResponse(debts=[to_debt_response(item) for item in items])
