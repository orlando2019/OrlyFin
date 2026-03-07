from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.settings.infrastructure.models import SystemSetting


# Modela la responsabilidad de 'settings repository' dentro del dominio o capa actual.
class SettingsRepository:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db

    # Obtiene 'by key' y lo expone para su uso en la capa llamadora.
    def get_by_key(self, organization_id: str, key: str) -> SystemSetting | None:
        return self.db.scalar(
            select(SystemSetting).where(SystemSetting.organization_id == organization_id, SystemSetting.key == key)
        )

    # Ejecuta la lógica principal de 'upsert' y devuelve el resultado esperado por el flujo.
    def upsert(
        self,
        organization_id: str,
        key: str,
        value: str,
        value_type: str,
        is_sensitive: bool,
    ) -> SystemSetting:
        existing = self.get_by_key(organization_id, key)
        if existing:
            existing.value = value
            existing.value_type = value_type
            existing.is_sensitive = is_sensitive
            self.db.flush()
            return existing

        setting = SystemSetting(
            organization_id=organization_id,
            key=key,
            value=value,
            value_type=value_type,
            is_sensitive=is_sensitive,
        )
        self.db.add(setting)
        self.db.flush()
        return setting

    # Lista 'for org' según los filtros o el contexto recibido.
    def list_for_org(self, organization_id: str) -> list[SystemSetting]:
        rows = self.db.scalars(
            select(SystemSetting)
            .where(SystemSetting.organization_id == organization_id)
            .order_by(SystemSetting.key.asc())
        ).all()
        return list(rows)
