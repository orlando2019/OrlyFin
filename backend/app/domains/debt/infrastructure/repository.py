from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domains.debt.infrastructure.models import DebtRecord


# Modela la responsabilidad de 'debt repository' dentro del dominio o capa actual.
class DebtRepository:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db

    # Ejecuta la lógica principal de 'create' y devuelve el resultado esperado por el flujo.
    def create(
        self,
        organization_id: str,
        account_id: str | None,
        creditor: str,
        description: str,
        principal_amount: Decimal,
        debt_type: str,
        total_installments: int | None,
        opened_on: date,
        due_on: date | None,
    ) -> DebtRecord:
        record = DebtRecord(
            organization_id=organization_id,
            account_id=account_id,
            creditor=creditor,
            description=description,
            principal_amount=principal_amount,
            balance_amount=principal_amount,
            debt_type=debt_type,
            total_installments=total_installments,
            paid_installments=0,
            opened_on=opened_on,
            due_on=due_on,
            status="active",
        )
        self.db.add(record)
        self.db.flush()
        return record

    # Obtiene 'by id for org' y lo expone para su uso en la capa llamadora.
    def get_by_id_for_org(self, debt_id: str, organization_id: str) -> DebtRecord | None:
        return self.db.scalar(
            select(DebtRecord).where(DebtRecord.id == debt_id, DebtRecord.organization_id == organization_id)
        )

    # Lista 'for org' según los filtros o el contexto recibido.
    def list_for_org(self, organization_id: str) -> list[DebtRecord]:
        rows = self.db.scalars(
            select(DebtRecord)
            .where(DebtRecord.organization_id == organization_id)
            .order_by(DebtRecord.opened_on.desc(), DebtRecord.created_at.desc())
        ).all()
        return list(rows)

    # Ejecuta la lógica principal de 'sum outstanding' y devuelve el resultado esperado por el flujo.
    def sum_outstanding(self, organization_id: str) -> Decimal:
        total = self.db.scalar(
            select(func.coalesce(func.sum(DebtRecord.balance_amount), 0)).where(
                DebtRecord.organization_id == organization_id,
                DebtRecord.status == "active",
            )
        )
        return Decimal(total or 0)

    # Ejecuta la lógica principal de 'count active' y devuelve el resultado esperado por el flujo.
    def count_active(self, organization_id: str) -> int:
        total = self.db.scalar(
            select(func.count(DebtRecord.id)).where(
                DebtRecord.organization_id == organization_id,
                DebtRecord.status == "active",
            )
        )
        return int(total or 0)
