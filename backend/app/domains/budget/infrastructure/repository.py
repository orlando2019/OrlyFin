from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.domains.budget.infrastructure.models import BudgetRecord


# Modela la responsabilidad de 'budget repository' dentro del dominio o capa actual.
class BudgetRepository:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db

    # Ejecuta la lógica principal de 'create' y devuelve el resultado esperado por el flujo.
    def create(
        self,
        organization_id: str,
        category: str,
        period_start: date,
        period_end: date,
        planned_amount: Decimal,
        alert_threshold_percent: Decimal,
    ) -> BudgetRecord:
        record = BudgetRecord(
            organization_id=organization_id,
            category=category,
            period_start=period_start,
            period_end=period_end,
            planned_amount=planned_amount,
            alert_threshold_percent=alert_threshold_percent,
            is_active=True,
        )
        self.db.add(record)
        self.db.flush()
        return record

    # Lista 'for org' según los filtros o el contexto recibido.
    def list_for_org(self, organization_id: str) -> list[BudgetRecord]:
        rows = self.db.scalars(
            select(BudgetRecord)
            .where(BudgetRecord.organization_id == organization_id)
            .order_by(BudgetRecord.period_start.desc(), BudgetRecord.created_at.desc())
        ).all()
        return list(rows)

    # Ejecuta la lógica principal de 'sum planned for overlap' y devuelve el resultado esperado por el flujo.
    def sum_planned_for_overlap(self, organization_id: str, start_on: date, end_on: date) -> Decimal:
        total = self.db.scalar(
            select(func.coalesce(func.sum(BudgetRecord.planned_amount), 0)).where(
                BudgetRecord.organization_id == organization_id,
                BudgetRecord.is_active.is_(True),
                and_(BudgetRecord.period_start <= end_on, BudgetRecord.period_end >= start_on),
            )
        )
        return Decimal(total or 0)
