"""Import all ORM models so they are registered in SQLAlchemy metadata."""

from app.domains.accounts.infrastructure.models import FinancialAccount
from app.domains.auth_users.infrastructure.models import Organization, User
from app.domains.budget.infrastructure.models import BudgetRecord
from app.domains.debt.infrastructure.models import DebtRecord
from app.domains.expense.infrastructure.models import ExpenseRecord
from app.domains.income.infrastructure.models import IncomeRecord
from app.domains.payment.infrastructure.models import PaymentRecord
from app.domains.rbac.infrastructure.models import Permission, Role, RolePermission, UserRole

__all__ = [
    "BudgetRecord",
    "DebtRecord",
    "ExpenseRecord",
    "FinancialAccount",
    "IncomeRecord",
    "Organization",
    "Permission",
    "PaymentRecord",
    "Role",
    "RolePermission",
    "User",
    "UserRole",
]
