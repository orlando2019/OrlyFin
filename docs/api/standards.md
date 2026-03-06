# Estándares API

## URL base
`/api/v1`

## Convenciones
- JSON para request/response.
- Fechas en ISO-8601.
- IDs en UUID.
- Montos en decimal y moneda ISO (`currency_code`).

## Idempotencia y trazabilidad
- Incluir `X-Request-Id` opcional.
- Responder `trace_id` en errores.

## Seguridad de sesión
- Access token y refresh token en cookies HttpOnly.
- Refresh con rotación en `/auth/refresh`.
