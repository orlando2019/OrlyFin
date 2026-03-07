# Estandares API

## Base y versionado
- Todas las rutas publicas deben iniciar en `/api/v1`.
- Cambios incompatibles requieren nueva version (`/api/v2`).

## Convenciones de diseno
- Formato: JSON en request/response (salvo carga de archivos).
- Fechas: ISO-8601.
- IDs: UUID string.
- Montos: decimal serializado como string.
- Recursos en plural (`/accounts`, `/incomes`, `/expenses`).

## Codigos HTTP esperados
- `200`: consulta/accion exitosa
- `201`: creacion exitosa
- `400`: validacion de payload
- `401`: sesion/token invalido o ausente
- `403`: permiso denegado
- `404`: recurso inexistente
- `409`: conflicto de negocio
- `429`: rate limit
- `500`: error interno no controlado

## Error estandar
Formato base:
- `code`
- `message`
- `details`
- `trace_id`
- `timestamp`

Referencia: `docs/api/error-model.md` y `contracts/errors/error-catalog.md`.

## Trazabilidad
- Cliente puede enviar `X-Request-Id`.
- Backend responde `X-Trace-Id`.
- Todo error debe incluir `trace_id`.

## Seguridad y permisos
- Auth con cookies HttpOnly (`access` y `refresh`).
- Endpoints protegidos validan permiso RBAC `module:action`.
- Matriz de referencia: `contracts/rbac/permissions-matrix.md`.

## Contratos
- Toda ruta nueva o cambio de schema debe reflejarse en `contracts/openapi/v1/openapi.yaml`.
- Ningun endpoint productivo debe quedar fuera de OpenAPI.
