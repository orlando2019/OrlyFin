from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    # Representa un detalle puntual de validación o regla de negocio.
    # `field` puede ser None cuando el error es global y no asociado a un atributo.
    field: str | None = None
    issue: str


class ErrorResponse(BaseModel):
    # Contrato estandarizado de error para toda la API.
    # Se usa tanto para errores de dominio (AppError) como para validaciones/500.
    code: str
    message: str
    details: list[dict[str, Any]] = Field(default_factory=list)
    trace_id: str
    timestamp: str


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int, details: list[dict[str, Any]] | None = None):
        # Excepción de negocio/controlada.
        # Parámetros:
        # - code: identificador estable para frontend/observabilidad (ej. UNAUTHORIZED).
        # - message: texto legible para cliente.
        # - status_code: código HTTP a devolver.
        # - details: lista opcional con contexto adicional por campo/regla.
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []


def build_error_response(code: str, message: str, trace_id: str, details: list[dict[str, Any]] | None = None) -> ErrorResponse:
    # Construye el payload final de error con timestamp UTC.
    # No persiste nada: solo transforma parámetros a un objeto consistente
    # para que los handlers de excepción devuelvan respuestas homogéneas.
    return ErrorResponse(
        code=code,
        message=message,
        details=details or [],
        trace_id=trace_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
