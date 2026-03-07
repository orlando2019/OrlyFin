from __future__ import annotations

import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings
from app.core.errors import AppError, build_error_response
from app.core.logging import get_logger
from app.domains.auth_users.application.service import AuthUsersService
from app.domains.rbac.application.service import RbacService
from app.interfaces.api.v1.router import router as api_v1_router
from app.shared.infrastructure.db.base import Base
from app.shared.infrastructure.db import model_registry as _model_registry  # noqa: F401
from app.shared.infrastructure.db.session import SessionLocal, engine

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Orquesta tareas de inicio/cierre de la app.
    # - Si DB_AUTO_CREATE_SCHEMA=true crea tablas usando los modelos registrados.
    # - Si BOOTSTRAP_SECURITY_DATA=true asegura permisos/roles base y usuario admin inicial.
    # No retorna datos; su efecto es dejar la plataforma lista antes de aceptar requests.
    if settings.db_auto_create_schema:
        Base.metadata.create_all(bind=engine)

    if settings.bootstrap_security_data:
        db = SessionLocal()
        try:
            RbacService(db).ensure_default_permissions_and_roles()
            AuthUsersService(db).ensure_bootstrap_data()
        finally:
            db.close()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    # Genera/propaga un identificador de traza por request y mide duración de punta a punta.
    # Entradas:
    # - request: objeto HTTP entrante.
    # - call_next: callback de FastAPI para continuar el pipeline.
    # Efectos:
    # - Guarda trace_id en request.state para que handlers/dependencias lo reutilicen.
    # - Expone X-Trace-Id en la respuesta para correlación cliente-servidor.
    # - Emite log estructurado con ruta, método, estado y latencia.
    trace_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    request.state.trace_id = trace_id
    start = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Trace-Id"] = trace_id

    logger.info(
        "http_request",
        extra={
            "trace_id": trace_id,
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code,
            "duration_ms": elapsed_ms,
        },
    )
    return response


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    # Aplica cabeceras mínimas de hardening OWASP en todas las respuestas.
    # Este middleware no valida payloads; su propósito es reducir vectores comunes
    # como MIME sniffing, clickjacking y fuga de referer.
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    # Traduce errores de negocio/controlados a un contrato JSON uniforme.
    # Mantiene code/message/details definidos por la capa de dominio y añade trace_id
    # para diagnóstico transversal entre logs y respuesta cliente.
    payload = build_error_response(
        code=exc.code,
        message=exc.message,
        details=exc.details,
        trace_id=getattr(request.state, "trace_id", str(uuid.uuid4())),
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Normaliza errores de validación de FastAPI/Pydantic al contrato estándar de API.
    # Convierte cada error en {field, issue} para que frontend pueda mostrar feedback
    # por campo sin depender del formato interno del framework.
    details = [{"field": ".".join(map(str, err["loc"])), "issue": err["msg"]} for err in exc.errors()]
    payload = build_error_response(
        code="VALIDATION_ERROR",
        message="Validation failed",
        details=details,
        trace_id=getattr(request.state, "trace_id", str(uuid.uuid4())),
    )
    return JSONResponse(status_code=400, content=payload.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, _: Exception):
    # Fallback global para excepciones no controladas.
    # Evita filtrar detalles internos al cliente y mantiene un 500 consistente
    # con trace_id para investigar el incidente en logs.
    payload = build_error_response(
        code="INTERNAL_ERROR",
        message="Unexpected internal error",
        details=[],
        trace_id=getattr(request.state, "trace_id", str(uuid.uuid4())),
    )
    return JSONResponse(status_code=500, content=payload.model_dump())


app.include_router(api_v1_router, prefix=settings.api_v1_prefix)
