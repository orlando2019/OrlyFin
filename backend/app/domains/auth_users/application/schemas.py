from __future__ import annotations

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str


class UserCreateRequest(BaseModel):
    email: str
    full_name: str
    password: str = Field(min_length=8)
    role_names: list[str] = Field(default_factory=lambda: ["operator"])


class AuthUserResponse(BaseModel):
    id: str
    organization_id: str
    email: str
    full_name: str
    is_active: bool
    roles: list[str]
    permissions: list[str]
