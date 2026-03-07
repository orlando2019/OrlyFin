from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


# Modela la responsabilidad de 'money' dentro del dominio o capa actual.
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency_code: str

    # Helper interno que encapsula la lógica de 'ost init'.
    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("amount must be >= 0")
        if len(self.currency_code) != 3:
            raise ValueError("currency_code must be ISO-4217 alpha-3")
