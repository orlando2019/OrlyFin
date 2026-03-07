from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domains.accounts.infrastructure.models import FinancialAccount


# Modela la responsabilidad de 'account repository' dentro del dominio o capa actual.
class AccountRepository:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db

    # Obtiene 'by id for org' y lo expone para su uso en la capa llamadora.
    def get_by_id_for_org(self, account_id: str, organization_id: str) -> FinancialAccount | None:
        return self.db.scalar(
            select(FinancialAccount).where(
                FinancialAccount.id == account_id,
                FinancialAccount.organization_id == organization_id,
            )
        )

    # Obtiene 'by name for org' y lo expone para su uso en la capa llamadora.
    def get_by_name_for_org(self, name: str, organization_id: str) -> FinancialAccount | None:
        return self.db.scalar(
            select(FinancialAccount).where(
                FinancialAccount.name == name,
                FinancialAccount.organization_id == organization_id,
            )
        )

    # Ejecuta la lógica principal de 'create' y devuelve el resultado esperado por el flujo.
    def create(
        self,
        organization_id: str,
        name: str,
        account_type: str,
        currency_code: str,
        initial_balance: Decimal,
    ) -> FinancialAccount:
        account = FinancialAccount(
            organization_id=organization_id,
            name=name,
            account_type=account_type,
            currency_code=currency_code.upper(),
            current_balance=initial_balance,
            is_active=True,
        )
        self.db.add(account)
        self.db.flush()
        return account

    # Lista 'for org' según los filtros o el contexto recibido.
    def list_for_org(self, organization_id: str) -> list[FinancialAccount]:
        rows = self.db.scalars(
            select(FinancialAccount)
            .where(FinancialAccount.organization_id == organization_id)
            .order_by(FinancialAccount.created_at.desc())
        ).all()
        return list(rows)

    # Ejecuta la lógica principal de 'sum balances for org' y devuelve el resultado esperado por el flujo.
    def sum_balances_for_org(self, organization_id: str) -> Decimal:
        total = self.db.scalar(
            select(func.coalesce(func.sum(FinancialAccount.current_balance), 0)).where(
                FinancialAccount.organization_id == organization_id,
                FinancialAccount.is_active.is_(True),
            )
        )
        return Decimal(total or 0)
