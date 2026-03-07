from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_trace_id
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.interfaces.dependencies import require_permission
from app.domains.settings.application.schemas import SettingListResponse, SettingResponse, SettingUpsertRequest
from app.domains.settings.application.service import SettingsService, get_settings_service

router = APIRouter(prefix="/settings", tags=["settings"])


# Ejecuta la lógica principal de 'upsert setting' y devuelve el resultado esperado por el flujo.
@router.post("", response_model=SettingResponse, dependencies=[Depends(require_permission("settings", "update"))])
def upsert_setting(
    payload: SettingUpsertRequest,
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: SettingsService = Depends(get_settings_service),
) -> SettingResponse:
    setting = service.upsert_setting(
        organization_id=current_user.organization_id,
        actor_user_id=current_user.id,
        trace_id=trace_id,
        payload=payload,
    )
    return service.to_response(setting)


# Lista 'settings' según los filtros o el contexto recibido.
@router.get("", response_model=SettingListResponse, dependencies=[Depends(require_permission("settings", "read"))])
def list_settings(
    current_user: User = Depends(get_current_user),
    service: SettingsService = Depends(get_settings_service),
) -> SettingListResponse:
    settings = service.list_settings(current_user.organization_id)
    return SettingListResponse(settings=[service.to_response(item) for item in settings])


# Obtiene 'setting' y lo expone para su uso en la capa llamadora.
@router.get("/{key}", response_model=SettingResponse, dependencies=[Depends(require_permission("settings", "read"))])
def get_setting(
    key: str,
    current_user: User = Depends(get_current_user),
    service: SettingsService = Depends(get_settings_service),
) -> SettingResponse:
    setting = service.get_setting(current_user.organization_id, key)
    return service.to_response(setting)
