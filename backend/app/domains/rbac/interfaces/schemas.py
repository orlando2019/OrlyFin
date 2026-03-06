from __future__ import annotations

from pydantic import BaseModel, Field


class PermissionListResponse(BaseModel):
    permissions: list[str]


class AssignRoleRequest(BaseModel):
    role_names: list[str] = Field(default_factory=list)


class AssignRoleResponse(BaseModel):
    user_id: str
    roles: list[str]
