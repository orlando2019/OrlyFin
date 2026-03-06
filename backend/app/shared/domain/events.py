from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class DomainEvent:
    name: str
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
