# Catálogo Inicial de Errores

## Comunes
- `VALIDATION_ERROR` (400)
- `UNAUTHORIZED` (401)
- `FORBIDDEN` (403)
- `NOT_FOUND` (404)
- `CONFLICT` (409)
- `RATE_LIMITED` (429)
- `INTERNAL_ERROR` (500)

## Formato estándar
- `code`: identificador funcional del error.
- `message`: mensaje legible.
- `details`: lista opcional de errores de campo.
- `trace_id`: correlación para soporte.
- `timestamp`: instante del error en UTC.
