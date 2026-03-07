from __future__ import annotations

from pydantic import BaseModel, Field


# Modela la responsabilidad de 'permission list response' dentro del dominio o capa actual.
class PermissionListResponse(BaseModel):
    permissions: list[str]


# Modela la responsabilidad de 'assign role request' dentro del dominio o capa actual.
class AssignRoleRequest(BaseModel):
    role_names: list[str] = Field(default_factory=list)


# Modela la responsabilidad de 'assign role response' dentro del dominio o capa actual.
class AssignRoleResponse(BaseModel):
    user_id: str
    roles: list[str]
