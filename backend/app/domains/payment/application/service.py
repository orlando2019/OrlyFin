from __future__ import annotations

from decimal import Decimal

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.accounts.infrastructure.repository import AccountRepository
from app.domains.audit.application.service import AuditService
from app.domains.debt.infrastructure.repository import DebtRepository
from app.domains.expense.infrastructure.repository import ExpenseRepository
from app.domains.payment.application.schemas import PaymentCreateRequest, PaymentResponse
from app.domains.payment.infrastructure.models import PaymentRecord
from app.domains.payment.infrastructure.repository import PaymentRepository

ALLOWED_PAYMENT_TYPES = {"regular", "debt", "installment"}
ALLOWED_REFERENCE_TYPES = {None, "expense", "debt", "other"}


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PaymentRepository(db)
        self.accounts_repo = AccountRepository(db)
        self.expense_repo = ExpenseRepository(db)
        self.debt_repo = DebtRepository(db)
        self.audit = AuditService(db)

    def create_payment(
        self,
        organization_id: str,
        payload: PaymentCreateRequest,
        actor_user_id: str | None = None,
        trace_id: str | None = None,
    ) -> PaymentRecord:
        if payload.amount <= 0:
            raise AppError("VALIDATION_ERROR", "amount must be > 0", 400)
        if payload.payment_type not in ALLOWED_PAYMENT_TYPES:
            raise AppError("VALIDATION_ERROR", "Invalid payment_type", 400)
        if payload.reference_type not in ALLOWED_REFERENCE_TYPES:
            raise AppError("VALIDATION_ERROR", "Invalid reference_type", 400)

        account = self.accounts_repo.get_by_id_for_org(payload.account_id, organization_id)
        if account is None:
            raise AppError("NOT_FOUND", "Account not found", 404)

        current_balance = Decimal(account.current_balance)
        if current_balance < Decimal(payload.amount):
            raise AppError("CONFLICT", "Insufficient account balance", 409)

        account.current_balance = current_balance - Decimal(payload.amount)

        if payload.reference_type == "expense":
            if not payload.reference_id:
                raise AppError("VALIDATION_ERROR", "reference_id is required for expense payments", 400)
            expense = self.expense_repo.get_by_id_for_org(payload.reference_id, organization_id)
            if expense is None:
                raise AppError("NOT_FOUND", "Expense not found", 404)
            if Decimal(payload.amount) >= Decimal(expense.amount):
                expense.status = "paid"

        if payload.reference_type == "debt":
            if not payload.reference_id:
                raise AppError("VALIDATION_ERROR", "reference_id is required for debt payments", 400)
            debt = self.debt_repo.get_by_id_for_org(payload.reference_id, organization_id)
            if debt is None:
                raise AppError("NOT_FOUND", "Debt not found", 404)
            if debt.status != "active":
                raise AppError("CONFLICT", "Debt is not active", 409)

            new_balance = Decimal(debt.balance_amount) - Decimal(payload.amount)
            debt.balance_amount = max(new_balance, Decimal("0.00"))
            if payload.payment_type == "installment" and debt.total_installments:
                debt.paid_installments = min(debt.total_installments, debt.paid_installments + 1)
            if debt.balance_amount == 0:
                debt.status = "closed"

        payment = self.repo.create(
            organization_id=organization_id,
            account_id=payload.account_id,
            payment_type=payload.payment_type,
            amount=Decimal(payload.amount),
            paid_on=payload.paid_on,
            reference_type=payload.reference_type,
            reference_id=payload.reference_id,
            notes=payload.notes,
        )

        if actor_user_id:
            self.audit.record_event(
                organization_id=organization_id,
                user_id=actor_user_id,
                module="payment",
                action="create",
                entity_type="payment_record",
                entity_id=payment.id,
                trace_id=trace_id,
                details={
                    "payment_type": payload.payment_type,
                    "amount": str(payload.amount),
                    "reference_type": payload.reference_type,
                    "reference_id": payload.reference_id,
                },
            )

        self.db.commit()
        return payment

    def list_payments(self, organization_id: str) -> list[PaymentRecord]:
        return self.repo.list_for_org(organization_id)



def to_payment_response(record: PaymentRecord) -> PaymentResponse:
    return PaymentResponse(
        id=record.id,
        organization_id=record.organization_id,
        account_id=record.account_id,
        payment_type=record.payment_type,
        amount=Decimal(record.amount),
        paid_on=record.paid_on,
        reference_type=record.reference_type,
        reference_id=record.reference_id,
        notes=record.notes,
    )



def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    return PaymentService(db)
