from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.errors import AppError
from app.domains.auth_users.application.service import get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.application.service import RbacService


def get_rbac_service(db: Session = Depends(get_db)) -> RbacService:
    return RbacService(db)


def require_permission(module: str, action: str) -> Callable:
    def checker(
        current_user: User = Depends(get_current_user),
        rbac_service: RbacService = Depends(get_rbac_service),
    ) -> User:
        if not rbac_service.has_permission(current_user.id, module, action):
            raise AppError("FORBIDDEN", "Permission denied", 403)
        return current_user

    return checker
