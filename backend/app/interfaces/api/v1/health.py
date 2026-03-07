from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from app.interfaces.schemas.common import HealthResponse

router = APIRouter()


# Ejecuta la lógica principal de 'health check' y devuelve el resultado esperado por el flujo.
@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="orlyfin-api",
        version="v1",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
