from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from app.core.config import settings


# Modela la responsabilidad de 'json formatter' dentro del dominio o capa actual.
class JsonFormatter(logging.Formatter):
    # Ejecuta la lógica principal de 'format' y devuelve el resultado esperado por el flujo.
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        extra_fields = {
            key: value
            for key, value in record.__dict__.items()
            if key
            not in {
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
            }
        }
        payload.update(extra_fields)
        return json.dumps(payload)


# Ejecuta la lógica principal de 'configure logging' y devuelve el resultado esperado por el flujo.
def configure_logging() -> None:
    root = logging.getLogger()
    if root.handlers:
        return

    root.setLevel(settings.log_level.upper())
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root.addHandler(handler)


# Obtiene 'logger' y lo expone para su uso en la capa llamadora.
def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
