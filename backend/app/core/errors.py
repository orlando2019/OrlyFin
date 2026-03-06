from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    field: str | None = None
    issue: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: list[dict[str, Any]] = Field(default_factory=list)
    trace_id: str
    timestamp: str


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int, details: list[dict[str, Any]] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []


def build_error_response(code: str, message: str, trace_id: str, details: list[dict[str, Any]] | None = None) -> ErrorResponse:
    return ErrorResponse(
        code=code,
        message=message,
        details=details or [],
        trace_id=trace_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
