from __future__ import annotations

import hashlib
import re
import uuid
from pathlib import Path

from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.attachments.application.schemas import AttachmentResponse
from app.domains.attachments.infrastructure.models import AttachmentRecord
from app.domains.attachments.infrastructure.repository import AttachmentRepository
from app.domains.audit.application.service import AuditService
from app.shared.infrastructure.storage.local_provider import LocalStorageProvider

_SAFE_FILENAME = re.compile(r"[^a-zA-Z0-9._-]+")


class AttachmentsService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AttachmentRepository(db)
        self.audit = AuditService(db)
        self.storage = LocalStorageProvider(base_path=settings.attachments_storage_path)

    def _safe_name(self, file_name: str) -> str:
        name = Path(file_name).name
        cleaned = _SAFE_FILENAME.sub("_", name)
        return cleaned[:200] if cleaned else "file"

    def _validate_file(self, mime_type: str, size_bytes: int) -> None:
        max_bytes = settings.attachment_max_size_mb * 1024 * 1024
        if size_bytes <= 0:
            raise AppError("VALIDATION_ERROR", "Attachment file is empty", 400)
        if size_bytes > max_bytes:
            raise AppError("VALIDATION_ERROR", f"Attachment exceeds {settings.attachment_max_size_mb} MB", 400)
        if mime_type not in settings.attachment_allowed_mime_types:
            raise AppError("VALIDATION_ERROR", "Attachment mime type is not allowed", 400)

    async def upload_attachment(
        self,
        organization_id: str,
        actor_user_id: str,
        trace_id: str,
        module: str,
        entity_id: str,
        file: UploadFile,
    ) -> AttachmentRecord:
        data = await file.read()
        mime_type = file.content_type or "application/octet-stream"
        self._validate_file(mime_type, len(data))

        checksum = hashlib.sha256(data).hexdigest()
        safe_name = self._safe_name(file.filename or "attachment")
        storage_rel_path = f"{organization_id}/{module}/{entity_id}/{uuid.uuid4().hex}_{safe_name}"
        self.storage.save(storage_rel_path, data)

        record = self.repo.create(
            organization_id=organization_id,
            uploaded_by_user_id=actor_user_id,
            module=module,
            entity_id=entity_id,
            file_name=safe_name,
            mime_type=mime_type,
            size_bytes=len(data),
            storage_path=storage_rel_path,
            checksum_sha256=checksum,
        )

        self.audit.record_event(
            organization_id=organization_id,
            user_id=actor_user_id,
            module="attachments",
            action="upload",
            entity_type="attachment",
            entity_id=record.id,
            trace_id=trace_id,
            details={"module": module, "entity_id": entity_id, "mime_type": mime_type, "size_bytes": len(data)},
        )

        self.db.commit()
        return record

    def delete_attachment(self, organization_id: str, actor_user_id: str, trace_id: str, attachment_id: str) -> AttachmentRecord:
        record = self.repo.get_by_id_for_org(attachment_id, organization_id)
        if record is None:
            raise AppError("NOT_FOUND", "Attachment not found", 404)
        if record.status == "deleted":
            return record

        self.storage.delete(record.storage_path)
        record.status = "deleted"

        self.audit.record_event(
            organization_id=organization_id,
            user_id=actor_user_id,
            module="attachments",
            action="delete",
            entity_type="attachment",
            entity_id=record.id,
            trace_id=trace_id,
            details={"module": record.module, "entity_id": record.entity_id},
        )
        self.db.commit()
        return record

    def list_attachments(self, organization_id: str, module: str | None = None, entity_id: str | None = None) -> list[AttachmentRecord]:
        return self.repo.list_for_org(organization_id, module=module, entity_id=entity_id)



def to_attachment_response(record: AttachmentRecord) -> AttachmentResponse:
    return AttachmentResponse(
        id=record.id,
        module=record.module,
        entity_id=record.entity_id,
        file_name=record.file_name,
        mime_type=record.mime_type,
        size_bytes=record.size_bytes,
        status=record.status,
    )



def get_attachments_service(db: Session = Depends(get_db)) -> AttachmentsService:
    return AttachmentsService(db)
