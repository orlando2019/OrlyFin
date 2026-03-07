from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


# Modela la responsabilidad de 'domain event' dentro del dominio o capa actual.
@dataclass(frozen=True)
class DomainEvent:
    name: str
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
