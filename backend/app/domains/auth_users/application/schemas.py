from __future__ import annotations

from pydantic import BaseModel, Field


# Modela la responsabilidad de 'login request' dentro del dominio o capa actual.
class LoginRequest(BaseModel):
    email: str
    password: str


# Modela la responsabilidad de 'user create request' dentro del dominio o capa actual.
class UserCreateRequest(BaseModel):
    email: str
    full_name: str
    password: str = Field(min_length=8)
    role_names: list[str] = Field(default_factory=lambda: ["operator"])


# Modela la responsabilidad de 'auth user response' dentro del dominio o capa actual.
class AuthUserResponse(BaseModel):
    id: str
    organization_id: str
    email: str
    full_name: str
    is_active: bool
    roles: list[str]
    permissions: list[str]
