from __future__ import annotations

from dataclasses import dataclass


# Modela la responsabilidad de 'authenticated user' dentro del dominio o capa actual.
@dataclass(frozen=True)
class AuthenticatedUser:
    id: str
    organization_id: str
    email: str
    is_active: bool
