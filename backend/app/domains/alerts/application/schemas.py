from __future__ import annotations

from pydantic import BaseModel


# Modela la responsabilidad de 'alert response' dentro del dominio o capa actual.
class AlertResponse(BaseModel):
    id: str
    module: str
    severity: str
    channel: str
    title: str
    message: str
    reference_type: str | None
    reference_id: str | None
    status: str
    triggered_on: str
    read_on: str | None


# Modela la responsabilidad de 'alert list response' dentro del dominio o capa actual.
class AlertListResponse(BaseModel):
    alerts: list[AlertResponse]


# Modela la responsabilidad de 'evaluate alerts response' dentro del dominio o capa actual.
class EvaluateAlertsResponse(BaseModel):
    generated: int
