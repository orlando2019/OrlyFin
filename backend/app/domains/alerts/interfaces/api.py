from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_trace_id
from app.domains.alerts.application.schemas import AlertListResponse, AlertResponse, EvaluateAlertsResponse
from app.domains.alerts.application.service import AlertsService, get_alerts_service, to_alert_response
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/alerts", tags=["alerts"])


# Ejecuta la lógica principal de 'evaluate alerts' y devuelve el resultado esperado por el flujo.
@router.post("/evaluate", response_model=EvaluateAlertsResponse, dependencies=[Depends(require_permission("alerts", "create"))])
def evaluate_alerts(
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: AlertsService = Depends(get_alerts_service),
) -> EvaluateAlertsResponse:
    generated = service.evaluate_alerts(current_user.organization_id, current_user.id, trace_id)
    return EvaluateAlertsResponse(generated=generated)


# Lista 'alerts' según los filtros o el contexto recibido.
@router.get("", response_model=AlertListResponse, dependencies=[Depends(require_permission("alerts", "read"))])
def list_alerts(
    status: str | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    service: AlertsService = Depends(get_alerts_service),
) -> AlertListResponse:
    alerts = service.list_alerts(current_user.organization_id, status=status)
    return AlertListResponse(alerts=[to_alert_response(item) for item in alerts])


# Ejecuta la lógica principal de 'mark alert read' y devuelve el resultado esperado por el flujo.
@router.post("/{alert_id}/read", response_model=AlertResponse, dependencies=[Depends(require_permission("alerts", "update"))])
def mark_alert_read(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: AlertsService = Depends(get_alerts_service),
) -> AlertResponse:
    alert = service.mark_read(current_user.organization_id, alert_id, current_user.id, trace_id)
    return to_alert_response(alert)
