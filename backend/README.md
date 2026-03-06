# Backend (FastAPI)

API REST versionada para OrlyFin.

## Base implementada en Fase 1
- Entry point FastAPI.
- Endpoint `GET /api/v1/health`.
- Manejo estandarizado de errores.
- Logging estructurado con `trace_id`.
- Configuración por variables de entorno.
- Base SQLAlchemy/Alembic preparada para módulos.

## Ejecutar
```bash
pip install -e .[dev]
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Estructura
- `app/core`: transversal.
- `app/interfaces`: REST y schemas.
- `app/shared`: componentes compartidos.
- `app/domains`: módulos de negocio.
