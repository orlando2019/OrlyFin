from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_trace_id
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.budget.application.schemas import BudgetCreateRequest, BudgetListResponse
from app.domains.budget.application.service import BudgetService, get_budget_service
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/budgets", tags=["budget"])


# Crea 'budget' aplicando las validaciones de negocio correspondientes.
@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("budget", "create"))])
def create_budget(
    payload: BudgetCreateRequest,
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: BudgetService = Depends(get_budget_service),
):
    record = service.create_budget(current_user.organization_id, payload, actor_user_id=current_user.id, trace_id=trace_id)
    return service.to_budget_response(current_user.organization_id, record)


# Lista 'budgets' según los filtros o el contexto recibido.
@router.get("", response_model=BudgetListResponse, dependencies=[Depends(require_permission("budget", "read"))])
def list_budgets(
    current_user: User = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
) -> BudgetListResponse:
    items = service.list_budgets(current_user.organization_id)
    return BudgetListResponse(budgets=[service.to_budget_response(current_user.organization_id, item) for item in items])
