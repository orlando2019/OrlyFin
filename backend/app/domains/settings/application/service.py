from __future__ import annotations

import json
from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.audit.application.service import AuditService
from app.domains.settings.application.schemas import SettingResponse, SettingUpsertRequest
from app.domains.settings.infrastructure.models import SystemSetting
from app.domains.settings.infrastructure.repository import SettingsRepository

SUPPORTED_TYPES = {"string", "int", "float", "bool", "json"}


class SettingsService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SettingsRepository(db)
        self.audit = AuditService(db)

    def _serialize(self, value_type: str, value: Any) -> str:
        if value_type == "string":
            return str(value)
        if value_type == "int":
            return str(int(value))
        if value_type == "float":
            return str(float(value))
        if value_type == "bool":
            return "true" if bool(value) else "false"
        if value_type == "json":
            return json.dumps(value, ensure_ascii=True)
        raise AppError("VALIDATION_ERROR", "Unsupported value_type", 400)

    def _deserialize(self, value_type: str, value: str) -> Any:
        if value_type == "string":
            return value
        if value_type == "int":
            return int(value)
        if value_type == "float":
            return float(value)
        if value_type == "bool":
            return value.lower() == "true"
        if value_type == "json":
            return json.loads(value)
        return value

    def upsert_setting(
        self,
        organization_id: str,
        actor_user_id: str,
        trace_id: str,
        payload: SettingUpsertRequest,
    ) -> SystemSetting:
        value_type = payload.value_type.lower().strip()
        if value_type not in SUPPORTED_TYPES:
            raise AppError("VALIDATION_ERROR", "Unsupported value_type", 400)

        serialized = self._serialize(value_type, payload.value)
        setting = self.repo.upsert(
            organization_id=organization_id,
            key=payload.key.strip(),
            value=serialized,
            value_type=value_type,
            is_sensitive=payload.is_sensitive,
        )
        self.audit.record_event(
            organization_id=organization_id,
            user_id=actor_user_id,
            module="settings",
            action="upsert",
            entity_type="system_setting",
            entity_id=setting.id,
            trace_id=trace_id,
            details={"key": setting.key, "value_type": setting.value_type, "is_sensitive": setting.is_sensitive},
        )
        self.db.commit()
        return setting

    def get_setting(self, organization_id: str, key: str) -> SystemSetting:
        setting = self.repo.get_by_key(organization_id, key)
        if setting is None:
            raise AppError("NOT_FOUND", "Setting not found", 404)
        return setting

    def list_settings(self, organization_id: str) -> list[SystemSetting]:
        return self.repo.list_for_org(organization_id)

    def to_response(self, setting: SystemSetting) -> SettingResponse:
        value = None if setting.is_sensitive else self._deserialize(setting.value_type, setting.value)
        return SettingResponse(
            key=setting.key,
            value=value,
            value_type=setting.value_type,
            is_sensitive=setting.is_sensitive,
        )



def get_settings_service(db: Session = Depends(get_db)) -> SettingsService:
    return SettingsService(db)
