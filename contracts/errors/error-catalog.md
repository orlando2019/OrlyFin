# Catalogo Inicial de Errores

## Comunes
- `VALIDATION_ERROR` (400)
- `UNAUTHORIZED` (401)
- `FORBIDDEN` (403)
- `NOT_FOUND` (404)
- `CONFLICT` (409)
- `RATE_LIMITED` (429)
- `INTERNAL_ERROR` (500)

## Seguridad/Auth
- `UNAUTHORIZED`: token ausente, token invalido, credenciales invalidas.
- `FORBIDDEN`: usuario autenticado sin permiso `module:action`.

## Formato estandar
- `code`
- `message`
- `details`
- `trace_id`
- `timestamp`
