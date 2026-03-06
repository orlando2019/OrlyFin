from __future__ import annotations

from pydantic import BaseModel


class AuthMessageResponse(BaseModel):
    message: str


class MeResponse(BaseModel):
    id: str
    organization_id: str
    email: str
    full_name: str
    roles: list[str]
    permissions: list[str]
