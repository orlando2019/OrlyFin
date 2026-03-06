from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domains.accounts.infrastructure.models import FinancialAccount


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_for_org(self, account_id: str, organization_id: str) -> FinancialAccount | None:
        return self.db.scalar(
            select(FinancialAccount).where(
                FinancialAccount.id == account_id,
                FinancialAccount.organization_id == organization_id,
            )
        )

    def get_by_name_for_org(self, name: str, organization_id: str) -> FinancialAccount | None:
        return self.db.scalar(
            select(FinancialAccount).where(
                FinancialAccount.name == name,
                FinancialAccount.organization_id == organization_id,
            )
        )

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

    def list_for_org(self, organization_id: str) -> list[FinancialAccount]:
        rows = self.db.scalars(
            select(FinancialAccount)
            .where(FinancialAccount.organization_id == organization_id)
            .order_by(FinancialAccount.created_at.desc())
        ).all()
        return list(rows)

    def sum_balances_for_org(self, organization_id: str) -> Decimal:
        total = self.db.scalar(
            select(func.coalesce(func.sum(FinancialAccount.current_balance), 0)).where(
                FinancialAccount.organization_id == organization_id,
                FinancialAccount.is_active.is_(True),
            )
        )
        return Decimal(total or 0)
