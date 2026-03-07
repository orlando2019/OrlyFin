from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_trace_id
from app.domains.accounts.application.schemas import AccountCreateRequest, AccountListResponse
from app.domains.accounts.application.service import AccountsService, get_accounts_service, to_account_response
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("accounts", "create"))],
)
# Crea 'account' aplicando las validaciones de negocio correspondientes.
def create_account(
    payload: AccountCreateRequest,
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: AccountsService = Depends(get_accounts_service),
):
    account = service.create_account(current_user.organization_id, payload, actor_user_id=current_user.id, trace_id=trace_id)
    return to_account_response(account)


# Lista 'accounts' según los filtros o el contexto recibido.
@router.get("", response_model=AccountListResponse, dependencies=[Depends(require_permission("accounts", "read"))])
def list_accounts(
    current_user: User = Depends(get_current_user),
    service: AccountsService = Depends(get_accounts_service),
) -> AccountListResponse:
    accounts = service.list_accounts(current_user.organization_id)
    return AccountListResponse(accounts=[to_account_response(item) for item in accounts])
