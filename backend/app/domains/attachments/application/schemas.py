from __future__ import annotations

from pydantic import BaseModel


class AttachmentResponse(BaseModel):
    id: str
    module: str
    entity_id: str
    file_name: str
    mime_type: str
    size_bytes: int
    status: str


class AttachmentListResponse(BaseModel):
    attachments: list[AttachmentResponse]
