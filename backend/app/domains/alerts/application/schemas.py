from __future__ import annotations

from pydantic import BaseModel


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


class AlertListResponse(BaseModel):
    alerts: list[AlertResponse]


class EvaluateAlertsResponse(BaseModel):
    generated: int
