from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.payment.application.schemas import PaymentCreateRequest, PaymentListResponse
from app.domains.payment.application.service import PaymentService, get_payment_service, to_payment_response
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/payments", tags=["payment"])


@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("payment", "create"))])
def create_payment(
    payload: PaymentCreateRequest,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
):
    record = service.create_payment(current_user.organization_id, payload)
    return to_payment_response(record)


@router.get("", response_model=PaymentListResponse, dependencies=[Depends(require_permission("payment", "read"))])
def list_payments(
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
) -> PaymentListResponse:
    items = service.list_payments(current_user.organization_id)
    return PaymentListResponse(payments=[to_payment_response(item) for item in items])
