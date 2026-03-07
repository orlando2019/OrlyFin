# Backend (FastAPI)

API REST versionada para OrlyFin.

## Base implementada en Fase 1
- Entry point FastAPI.
- Endpoint `GET /api/v1/health`.
- Manejo estandarizado de errores.
- Logging estructurado con `trace_id`.
- Configuración por variables de entorno.
- Base SQLAlchemy/Alembic preparada para módulos.

## Base implementada en Fase 2
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `POST /api/v1/users` (protegido por permiso `auth_users:create`)
- `GET /api/v1/rbac/me/permissions`
- `POST /api/v1/rbac/users/{user_id}/roles` (protegido por permiso `rbac:update`)

## Base implementada en Fase 3
- `POST/GET /api/v1/accounts`
- `POST/GET /api/v1/incomes`
- `POST/GET /api/v1/expenses`
- `POST/GET /api/v1/debts`
- `POST/GET /api/v1/payments`
- `POST/GET /api/v1/budgets`
- `GET /api/v1/dashboard/executive`

## Base implementada en Fase 4
- `POST/GET /api/v1/reconciliations`
- `POST /api/v1/reconciliations/{reconciliation_id}/resolve`
- `POST /api/v1/alerts/evaluate`
- `GET /api/v1/alerts`
- `POST /api/v1/alerts/{alert_id}/read`
- `GET /api/v1/audit/events`
- `POST /api/v1/attachments/upload`
- `GET /api/v1/attachments`
- `DELETE /api/v1/attachments/{attachment_id}`
- `POST/GET /api/v1/settings`
- `GET /api/v1/settings/{key}`

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
