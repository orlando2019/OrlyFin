from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domains.expense.infrastructure.models import ExpenseRecord


# Modela la responsabilidad de 'expense repository' dentro del dominio o capa actual.
class ExpenseRepository:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db

    # Ejecuta la lógica principal de 'create' y devuelve el resultado esperado por el flujo.
    def create(
        self,
        organization_id: str,
        account_id: str | None,
        category: str,
        description: str,
        amount: Decimal,
        expense_type: str,
        due_on: date | None,
        occurred_on: date,
        status: str,
    ) -> ExpenseRecord:
        record = ExpenseRecord(
            organization_id=organization_id,
            account_id=account_id,
            category=category,
            description=description,
            amount=amount,
            expense_type=expense_type,
            due_on=due_on,
            occurred_on=occurred_on,
            status=status,
        )
        self.db.add(record)
        self.db.flush()
        return record

    # Obtiene 'by id for org' y lo expone para su uso en la capa llamadora.
    def get_by_id_for_org(self, expense_id: str, organization_id: str) -> ExpenseRecord | None:
        return self.db.scalar(
            select(ExpenseRecord).where(
                ExpenseRecord.id == expense_id,
                ExpenseRecord.organization_id == organization_id,
            )
        )

    # Lista 'for org' según los filtros o el contexto recibido.
    def list_for_org(self, organization_id: str) -> list[ExpenseRecord]:
        rows = self.db.scalars(
            select(ExpenseRecord)
            .where(ExpenseRecord.organization_id == organization_id)
            .order_by(ExpenseRecord.occurred_on.desc(), ExpenseRecord.created_at.desc())
        ).all()
        return list(rows)

    # Ejecuta la lógica principal de 'sum for period' y devuelve el resultado esperado por el flujo.
    def sum_for_period(self, organization_id: str, start_on: date, end_on: date) -> Decimal:
        total = self.db.scalar(
            select(func.coalesce(func.sum(ExpenseRecord.amount), 0)).where(
                ExpenseRecord.organization_id == organization_id,
                ExpenseRecord.occurred_on >= start_on,
                ExpenseRecord.occurred_on <= end_on,
            )
        )
        return Decimal(total or 0)

    # Ejecuta la lógica principal de 'sum by category period' y devuelve el resultado esperado por el flujo.
    def sum_by_category_period(self, organization_id: str, category: str, start_on: date, end_on: date) -> Decimal:
        total = self.db.scalar(
            select(func.coalesce(func.sum(ExpenseRecord.amount), 0)).where(
                ExpenseRecord.organization_id == organization_id,
                ExpenseRecord.category == category,
                ExpenseRecord.occurred_on >= start_on,
                ExpenseRecord.occurred_on <= end_on,
                ExpenseRecord.status != "cancelled",
            )
        )
        return Decimal(total or 0)

    # Ejecuta la lógica principal de 'count pending' y devuelve el resultado esperado por el flujo.
    def count_pending(self, organization_id: str) -> int:
        total = self.db.scalar(
            select(func.count(ExpenseRecord.id)).where(
                ExpenseRecord.organization_id == organization_id,
                ExpenseRecord.status == "pending",
            )
        )
        return int(total or 0)
