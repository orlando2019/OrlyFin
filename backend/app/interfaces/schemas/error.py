from typing import Any

from pydantic import BaseModel, Field


class ErrorResponseSchema(BaseModel):
    code: str
    message: str
    details: list[dict[str, Any]] = Field(default_factory=list)
    trace_id: str
    timestamp: str
