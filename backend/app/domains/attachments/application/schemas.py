from __future__ import annotations

from pydantic import BaseModel


# Modela la responsabilidad de 'attachment response' dentro del dominio o capa actual.
class AttachmentResponse(BaseModel):
    id: str
    module: str
    entity_id: str
    file_name: str
    mime_type: str
    size_bytes: int
    status: str


# Modela la responsabilidad de 'attachment list response' dentro del dominio o capa actual.
class AttachmentListResponse(BaseModel):
    attachments: list[AttachmentResponse]
