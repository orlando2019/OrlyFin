from __future__ import annotations

from fastapi import APIRouter, Depends

from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.application.service import RbacService
from app.domains.rbac.interfaces.dependencies import get_rbac_service, require_permission
from app.domains.rbac.interfaces.schemas import AssignRoleRequest, AssignRoleResponse, PermissionListResponse

router = APIRouter(prefix="/rbac", tags=["rbac"])


@router.get("/me/permissions", response_model=PermissionListResponse)
def my_permissions(
    current_user: User = Depends(get_current_user),
    rbac_service: RbacService = Depends(get_rbac_service),
) -> PermissionListResponse:
    return PermissionListResponse(permissions=rbac_service.get_user_permission_keys(current_user.id))


@router.post(
    "/users/{user_id}/roles",
    response_model=AssignRoleResponse,
    dependencies=[Depends(require_permission("rbac", "update"))],
)
def assign_roles(
    user_id: str,
    payload: AssignRoleRequest,
    current_user: User = Depends(get_current_user),
    rbac_service: RbacService = Depends(get_rbac_service),
) -> AssignRoleResponse:
    rbac_service.assign_roles_to_user(user_id, payload.role_names, organization_id=current_user.organization_id)
    rbac_service.db.commit()
    return AssignRoleResponse(user_id=user_id, roles=rbac_service.get_user_roles(user_id))
