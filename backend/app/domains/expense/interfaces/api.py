from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_trace_id
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.expense.application.schemas import ExpenseCreateRequest, ExpenseListResponse
from app.domains.expense.application.service import ExpenseService, get_expense_service, to_expense_response
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/expenses", tags=["expense"])


# Crea 'expense' aplicando las validaciones de negocio correspondientes.
@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("expense", "create"))])
def create_expense(
    payload: ExpenseCreateRequest,
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: ExpenseService = Depends(get_expense_service),
):
    record = service.create_expense(current_user.organization_id, payload, actor_user_id=current_user.id, trace_id=trace_id)
    return to_expense_response(record)


# Lista 'expenses' según los filtros o el contexto recibido.
@router.get("", response_model=ExpenseListResponse, dependencies=[Depends(require_permission("expense", "read"))])
def list_expenses(
    current_user: User = Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
) -> ExpenseListResponse:
    items = service.list_expenses(current_user.organization_id)
    return ExpenseListResponse(expenses=[to_expense_response(item) for item in items])
