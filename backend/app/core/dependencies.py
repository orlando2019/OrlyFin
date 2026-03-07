from __future__ import annotations

from fastapi import Request
from sqlalchemy.orm import Session

from app.shared.infrastructure.db.session import SessionLocal


def get_trace_id(request: Request) -> str:
    # Extrae el trace_id inyectado por middleware para pasarlo a endpoints/servicios
    # que necesiten correlación de logs o respuestas. Si por alguna razón no existe,
    # retorna string vacío para no romper la resolución de dependencias.
    return getattr(request.state, "trace_id", "")


def get_db() -> Session:
    # Provee una sesión SQLAlchemy por request.
    # Flujo:
    # 1) Crea SessionLocal al entrar al endpoint.
    # 2) Entrega la sesión vía `yield` a repositorios/servicios.
    # 3) Cierra siempre en `finally` para evitar fugas de conexión.
    # Nota: la transacción (commit/rollback) se controla en la capa de aplicación.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
