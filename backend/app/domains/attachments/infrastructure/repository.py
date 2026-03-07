from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.attachments.infrastructure.models import AttachmentRecord


# Modela la responsabilidad de 'attachment repository' dentro del dominio o capa actual.
class AttachmentRepository:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db

    # Ejecuta la lógica principal de 'create' y devuelve el resultado esperado por el flujo.
    def create(
        self,
        organization_id: str,
        uploaded_by_user_id: str,
        module: str,
        entity_id: str,
        file_name: str,
        mime_type: str,
        size_bytes: int,
        storage_path: str,
        checksum_sha256: str,
    ) -> AttachmentRecord:
        record = AttachmentRecord(
            organization_id=organization_id,
            uploaded_by_user_id=uploaded_by_user_id,
            module=module,
            entity_id=entity_id,
            file_name=file_name,
            mime_type=mime_type,
            size_bytes=size_bytes,
            storage_path=storage_path,
            checksum_sha256=checksum_sha256,
            status="uploaded",
        )
        self.db.add(record)
        self.db.flush()
        return record

    # Obtiene 'by id for org' y lo expone para su uso en la capa llamadora.
    def get_by_id_for_org(self, attachment_id: str, organization_id: str) -> AttachmentRecord | None:
        return self.db.scalar(
            select(AttachmentRecord).where(
                AttachmentRecord.id == attachment_id,
                AttachmentRecord.organization_id == organization_id,
            )
        )

    # Lista 'for org' según los filtros o el contexto recibido.
    def list_for_org(self, organization_id: str, module: str | None = None, entity_id: str | None = None) -> list[AttachmentRecord]:
        query = select(AttachmentRecord).where(AttachmentRecord.organization_id == organization_id)
        if module:
            query = query.where(AttachmentRecord.module == module)
        if entity_id:
            query = query.where(AttachmentRecord.entity_id == entity_id)
        rows = self.db.scalars(query.order_by(AttachmentRecord.created_at.desc())).all()
        return list(rows)
