# Baseline de Seguridad

- Contraseñas con hash robusto (PBKDF2-HMAC-SHA256 con salt e iteraciones altas).
- JWT en cookies HttpOnly con expiraciones diferenciadas.
- Validación estricta de entradas.
- Control de CORS por ambiente.
- Rate limiting en endpoints sensibles (base aplicada en login).
- Auditoría para operaciones críticas.
