from __future__ import annotations

from pydantic import BaseModel


# Modela la responsabilidad de 'auth message response' dentro del dominio o capa actual.
class AuthMessageResponse(BaseModel):
    message: str


# Modela la responsabilidad de 'me response' dentro del dominio o capa actual.
class MeResponse(BaseModel):
    id: str
    organization_id: str
    email: str
    full_name: str
    roles: list[str]
    permissions: list[str]
