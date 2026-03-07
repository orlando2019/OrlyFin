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
    # Proveedor DI de RBAC para endpoints/dependencias que necesiten autorización.
    return RbacService(db)


def require_permission(module: str, action: str) -> Callable:
    # Fábrica de dependencia que encapsula autorización declarativa por endpoint.
    # Uso típico: Depends(require_permission("expense", "create")).
    # Retorna un `checker` que valida usuario actual contra RBAC antes de ejecutar handler.
    def checker(
        current_user: User = Depends(get_current_user),
        rbac_service: RbacService = Depends(get_rbac_service),
    ) -> User:
        # Si el usuario no tiene permiso explícito módulo:acción, aborta con 403.
        # Retorna el usuario para que el endpoint lo reutilice sin otra búsqueda.
        if not rbac_service.has_permission(current_user.id, module, action):
            raise AppError("FORBIDDEN", "Permission denied", 403)
        return current_user

    return checker
