from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from app.core.dependencies import get_trace_id
from app.domains.attachments.application.schemas import AttachmentListResponse, AttachmentResponse
from app.domains.attachments.application.service import AttachmentsService, get_attachments_service, to_attachment_response
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.interfaces.dependencies import require_permission

router = APIRouter(prefix="/attachments", tags=["attachments"])


# Ejecuta la lógica principal de 'upload attachment' y devuelve el resultado esperado por el flujo.
@router.post("/upload", response_model=AttachmentResponse, dependencies=[Depends(require_permission("attachments", "create"))])
async def upload_attachment(
    module: str = Form(...),
    entity_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: AttachmentsService = Depends(get_attachments_service),
) -> AttachmentResponse:
    record = await service.upload_attachment(
        organization_id=current_user.organization_id,
        actor_user_id=current_user.id,
        trace_id=trace_id,
        module=module,
        entity_id=entity_id,
        file=file,
    )
    return to_attachment_response(record)


# Ejecuta la lógica principal de 'delete attachment' y devuelve el resultado esperado por el flujo.
@router.delete("/{attachment_id}", response_model=AttachmentResponse, dependencies=[Depends(require_permission("attachments", "delete"))])
def delete_attachment(
    attachment_id: str,
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
    service: AttachmentsService = Depends(get_attachments_service),
) -> AttachmentResponse:
    record = service.delete_attachment(current_user.organization_id, current_user.id, trace_id, attachment_id)
    return to_attachment_response(record)


# Lista 'attachments' según los filtros o el contexto recibido.
@router.get("", response_model=AttachmentListResponse, dependencies=[Depends(require_permission("attachments", "read"))])
def list_attachments(
    module: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    service: AttachmentsService = Depends(get_attachments_service),
) -> AttachmentListResponse:
    rows = service.list_attachments(current_user.organization_id, module=module, entity_id=entity_id)
    return AttachmentListResponse(attachments=[to_attachment_response(item) for item in rows])
