# Modelo de Error

Estructura estándar:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Validation failed",
  "details": [{"field": "email", "issue": "invalid_format"}],
  "trace_id": "c4e7d0b9-0c58-4b17-a548-2db8f5db8cd7",
  "timestamp": "2026-03-05T23:00:00Z"
}
```

Campos obligatorios: `code`, `message`, `trace_id`, `timestamp`.
