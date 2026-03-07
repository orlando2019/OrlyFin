from __future__ import annotations

import threading
import time
from collections import defaultdict
from collections.abc import Callable

from fastapi import Depends, Request

from app.core.errors import AppError

_RATE_STATE: dict[str, list[float]] = defaultdict(list)
_RATE_LOCK = threading.Lock()


# Ejecuta la lógica principal de 'limit requests' y devuelve el resultado esperado por el flujo.
def limit_requests(key_prefix: str, limit: int, window_seconds: int) -> Callable:
    # Ejecuta la lógica principal de 'dependency' y devuelve el resultado esperado por el flujo.
    def dependency(request: Request) -> None:
        client_ip = request.client.host if request.client else "unknown"
        key = f"{key_prefix}:{client_ip}"
        now = time.time()

        with _RATE_LOCK:
            timestamps = _RATE_STATE[key]
            valid = [ts for ts in timestamps if now - ts < window_seconds]
            if len(valid) >= limit:
                raise AppError("RATE_LIMITED", "Too many requests", 429)
            valid.append(now)
            _RATE_STATE[key] = valid

    return Depends(dependency)
