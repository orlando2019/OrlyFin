from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_trace_id
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.income.application.schemas import IncomeCreateRequest, IncomeListResponse
from app.domains.income.application.service import IncomeService, get_income_service, to_income_response
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/incomes", tags=["income"])


@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("income", "create"))])
def create_income(
    payload: IncomeCreateRequest,
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: IncomeService = Depends(get_income_service),
):
    record = service.create_income(current_user.organization_id, payload, actor_user_id=current_user.id, trace_id=trace_id)
    return to_income_response(record)


@router.get("", response_model=IncomeListResponse, dependencies=[Depends(require_permission("income", "read"))])
def list_incomes(
    current_user: User = Depends(get_current_user),
    service: IncomeService = Depends(get_income_service),
) -> IncomeListResponse:
    items = service.list_incomes(current_user.organization_id)
    return IncomeListResponse(incomes=[to_income_response(item) for item in items])
