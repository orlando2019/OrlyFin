from __future__ import annotations

from decimal import Decimal

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.audit.application.service import AuditService
from app.domains.accounts.infrastructure.repository import AccountRepository
from app.domains.debt.application.schemas import DebtCreateRequest, DebtResponse
from app.domains.debt.infrastructure.models import DebtRecord
from app.domains.debt.infrastructure.repository import DebtRepository

ALLOWED_DEBT_TYPES = {"simple", "installment"}


# Modela la responsabilidad de 'debt service' dentro del dominio o capa actual.
class DebtService:
    # Inicializa la instancia y prepara las dependencias necesarias para sus operaciones.
    def __init__(self, db: Session):
        self.db = db
        self.repo = DebtRepository(db)
        self.accounts_repo = AccountRepository(db)
        self.audit = AuditService(db)

    # Crea 'debt' aplicando las validaciones de negocio correspondientes.
    def create_debt(
        self,
        organization_id: str,
        payload: DebtCreateRequest,
        actor_user_id: str | None = None,
        trace_id: str | None = None,
    ) -> DebtRecord:
        if payload.principal_amount <= 0:
            raise AppError("VALIDATION_ERROR", "principal_amount must be > 0", 400)
        if payload.debt_type not in ALLOWED_DEBT_TYPES:
            raise AppError("VALIDATION_ERROR", "Invalid debt_type", 400)
        if payload.debt_type == "installment" and (payload.total_installments is None or payload.total_installments <= 0):
            raise AppError("VALIDATION_ERROR", "total_installments is required for installment debt", 400)

        if payload.account_id:
            account = self.accounts_repo.get_by_id_for_org(payload.account_id, organization_id)
            if account is None:
                raise AppError("NOT_FOUND", "Account not found", 404)

        record = self.repo.create(
            organization_id=organization_id,
            account_id=payload.account_id,
            creditor=payload.creditor,
            description=payload.description,
            principal_amount=Decimal(payload.principal_amount),
            debt_type=payload.debt_type,
            total_installments=payload.total_installments,
            opened_on=payload.opened_on,
            due_on=payload.due_on,
        )
        if actor_user_id:
            self.audit.record_event(
                organization_id=organization_id,
                user_id=actor_user_id,
                module="debt",
                action="create",
                entity_type="debt_record",
                entity_id=record.id,
                trace_id=trace_id,
                details={"creditor": payload.creditor, "principal_amount": str(payload.principal_amount)},
            )
        self.db.commit()
        return record

    # Lista 'debts' según los filtros o el contexto recibido.
    def list_debts(self, organization_id: str) -> list[DebtRecord]:
        return self.repo.list_for_org(organization_id)



# Transforma la entidad de dominio en la estructura de respuesta 'to debt response'.
def to_debt_response(record: DebtRecord) -> DebtResponse:
    return DebtResponse(
        id=record.id,
        organization_id=record.organization_id,
        account_id=record.account_id,
        creditor=record.creditor,
        description=record.description,
        principal_amount=Decimal(record.principal_amount),
        balance_amount=Decimal(record.balance_amount),
        debt_type=record.debt_type,
        total_installments=record.total_installments,
        paid_installments=record.paid_installments,
        opened_on=record.opened_on,
        due_on=record.due_on,
        status=record.status,
    )



# Obtiene 'debt service' y lo expone para su uso en la capa llamadora.
def get_debt_service(db: Session = Depends(get_db)) -> DebtService:
    return DebtService(db)
