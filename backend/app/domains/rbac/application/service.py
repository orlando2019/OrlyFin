from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.domain.constants import ACTIONS, MODULES
from app.domains.rbac.infrastructure.models import Permission, Role
from app.domains.rbac.infrastructure.repository import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    UserRoleRepository,
)


class RbacService:
    def __init__(self, db: Session):
        self.db = db
        self.role_repo = RoleRepository(db)
        self.permission_repo = PermissionRepository(db)
        self.user_role_repo = UserRoleRepository(db)
        self.role_permission_repo = RolePermissionRepository(db)

    def ensure_default_permissions_and_roles(self) -> None:
        for module in MODULES:
            for action in ACTIONS:
                if self.permission_repo.get_by_module_action(module, action) is None:
                    self.permission_repo.create(module, action)

        role_specs = {
            "owner_admin": "Full access over all modules",
            "admin": "Administrative access over operational modules",
            "operator": "Execution permissions over assigned modules",
            "viewer": "Read-only access",
        }

        for role_name, role_description in role_specs.items():
            if self.role_repo.get_by_name(role_name) is None:
                self.role_repo.create(role_name, role_description)

        self.db.flush()

        all_permission_ids = self.db.scalars(select(Permission.id)).all()
        admin_permission_ids = self.db.scalars(
            select(Permission.id).where(Permission.action.in_(["read", "create", "update", "delete", "export"]))
        ).all()
        operator_permission_ids = self.db.scalars(
            select(Permission.id).where(
                Permission.module.in_(["income", "expense", "debt", "payment", "budget", "accounts", "credit_cards"]),
                Permission.action.in_(["read", "create", "update"]),
            )
        ).all()
        viewer_permission_ids = self.db.scalars(select(Permission.id).where(Permission.action == "read")).all()

        mapping = {
            "owner_admin": list(all_permission_ids),
            "admin": list(admin_permission_ids),
            "operator": list(operator_permission_ids),
            "viewer": list(viewer_permission_ids),
        }

        for role_name, permission_ids in mapping.items():
            role = self.role_repo.get_by_name(role_name)
            if role is None:
                continue
            for permission_id in permission_ids:
                self.role_permission_repo.add(role.id, permission_id)

        self.db.commit()

    def assign_roles_to_user(self, user_id: str, role_names: list[str], organization_id: str) -> None:
        user = self.db.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise AppError("NOT_FOUND", "User not found", 404)
        if user.organization_id != organization_id:
            raise AppError("FORBIDDEN", "Cross-organization role assignment is not allowed", 403)

        normalized = list(dict.fromkeys([name.strip().lower() for name in role_names if name.strip()]))
        if not normalized:
            normalized = ["operator"]

        for role_name in normalized:
            role = self.role_repo.get_by_name(role_name)
            if role is None:
                raise AppError("VALIDATION_ERROR", f"Role '{role_name}' is not defined", 400)
            self.user_role_repo.add(user_id=user_id, role_id=role.id, organization_id=organization_id)

    def get_user_roles(self, user_id: str) -> list[str]:
        role_ids = self.user_role_repo.get_role_ids_for_user(user_id)
        if not role_ids:
            return []

        rows = self.db.scalars(select(Role.name).where(Role.id.in_(role_ids))).all()
        return sorted(set(rows))

    def get_user_permission_keys(self, user_id: str) -> list[str]:
        role_ids = self.user_role_repo.get_role_ids_for_user(user_id)
        permission_ids = self.role_permission_repo.get_permission_ids_for_roles(role_ids)
        if not permission_ids:
            return []

        permissions = self.db.scalars(select(Permission).where(Permission.id.in_(permission_ids))).all()
        keys = [f"{permission.module}:{permission.action}" for permission in permissions]
        return sorted(set(keys))

    def has_permission(self, user_id: str, module: str, action: str) -> bool:
        key = f"{module}:{action}"
        return key in self.get_user_permission_keys(user_id)
