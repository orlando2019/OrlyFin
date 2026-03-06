# Baseline de Seguridad

- Contraseñas con hash robusto (Argon2 o bcrypt con costo adecuado).
- JWT en cookies HttpOnly con expiraciones diferenciadas.
- Validación estricta de entradas.
- Control de CORS por ambiente.
- Rate limiting en endpoints sensibles.
- Auditoría para operaciones críticas.
