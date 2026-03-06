"""Import all ORM models so they are registered in SQLAlchemy metadata."""

from app.domains.auth_users.infrastructure.models import Organization, User
from app.domains.rbac.infrastructure.models import Permission, Role, RolePermission, UserRole

__all__ = [
    "Organization",
    "Permission",
    "Role",
    "RolePermission",
    "User",
    "UserRole",
]
