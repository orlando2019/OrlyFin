from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticatedUser:
    id: str
    organization_id: str
    email: str
    is_active: bool
