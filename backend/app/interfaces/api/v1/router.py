from fastapi import APIRouter

from app.domains.accounts.interfaces.api import router as accounts_router
from app.domains.alerts.interfaces.api import router as alerts_router
from app.domains.attachments.interfaces.api import router as attachments_router
from app.domains.audit.interfaces.api import router as audit_router
from app.domains.auth_users.interfaces.api import router as auth_router
from app.domains.auth_users.interfaces.api import users_router
from app.domains.budget.interfaces.api import router as budgets_router
from app.domains.dashboard.interfaces.api import router as dashboard_router
from app.domains.debt.interfaces.api import router as debts_router
from app.domains.expense.interfaces.api import router as expenses_router
from app.domains.income.interfaces.api import router as incomes_router
from app.domains.payment.interfaces.api import router as payments_router
from app.domains.rbac.interfaces.api import router as rbac_router
from app.domains.reconciliation.interfaces.api import router as reconciliation_router
from app.domains.settings.interfaces.api import router as settings_router
from app.interfaces.api.v1.health import router as health_router

router = APIRouter()
router.include_router(health_router, tags=["system"])
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(rbac_router)
router.include_router(accounts_router)
router.include_router(incomes_router)
router.include_router(expenses_router)
router.include_router(debts_router)
router.include_router(payments_router)
router.include_router(budgets_router)
router.include_router(dashboard_router)
router.include_router(reconciliation_router)
router.include_router(alerts_router)
router.include_router(audit_router)
router.include_router(attachments_router)
router.include_router(settings_router)
