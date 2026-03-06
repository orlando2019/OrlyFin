# ADR-003: JWT en Cookies HttpOnly

## Estado
Aceptado.

## Decisión
Autenticación basada en access token corto y refresh token rotativo en cookies HttpOnly.

## Justificación
- Reduce exposición de tokens frente a XSS.
- Compatible con experiencia web de sesión persistente.

## Consecuencia
Debe aplicarse política CSRF, expiración y revocación de refresh tokens.
