from __future__ import annotations

from fastapi import APIRouter, Depends

from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.dashboard.application.schemas import ExecutiveDashboardResponse
from app.domains.dashboard.application.service import DashboardService, get_dashboard_service
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    "/executive",
    response_model=ExecutiveDashboardResponse,
    dependencies=[Depends(require_permission("dashboard", "read"))],
)
# Obtiene 'executive dashboard' y lo expone para su uso en la capa llamadora.
def get_executive_dashboard(
    current_user: User = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
) -> ExecutiveDashboardResponse:
    return service.get_executive_summary(current_user.organization_id)
