from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.rbac.infrastructure.models import Permission, Role, RolePermission, UserRole


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Role | None:
        return self.db.scalar(select(Role).where(Role.name == name))

    def create(self, name: str, description: str) -> Role:
        role = Role(name=name, description=description)
        self.db.add(role)
        self.db.flush()
        return role


class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_module_action(self, module: str, action: str) -> Permission | None:
        return self.db.scalar(select(Permission).where(Permission.module == module, Permission.action == action))

    def create(self, module: str, action: str) -> Permission:
        permission = Permission(module=module, action=action)
        self.db.add(permission)
        self.db.flush()
        return permission


class UserRoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, user_id: str, role_id: str, organization_id: str) -> UserRole:
        existing = self.db.scalar(select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id))
        if existing:
            return existing

        user_role = UserRole(user_id=user_id, role_id=role_id, organization_id=organization_id)
        self.db.add(user_role)
        self.db.flush()
        return user_role

    def get_role_ids_for_user(self, user_id: str) -> list[str]:
        rows = self.db.scalars(select(UserRole.role_id).where(UserRole.user_id == user_id)).all()
        return list(rows)


class RolePermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, role_id: str, permission_id: str) -> RolePermission:
        existing = self.db.scalar(
            select(RolePermission).where(RolePermission.role_id == role_id, RolePermission.permission_id == permission_id)
        )
        if existing:
            return existing

        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        self.db.add(role_permission)
        self.db.flush()
        return role_permission

    def get_permission_ids_for_roles(self, role_ids: list[str]) -> list[str]:
        if not role_ids:
            return []
        rows = self.db.scalars(select(RolePermission.permission_id).where(RolePermission.role_id.in_(role_ids))).all()
        return list(set(rows))
