# Baseline de Seguridad

Linea base minima para operar OrlyFin por fases.

## Controles implementados
- Hash de contrasena con PBKDF2-HMAC-SHA256 + salt.
- Auth con cookies HttpOnly (`access` y `refresh`).
- Catalogo de errores y manejo centralizado.
- RBAC por modulo/accion.
- CORS configurable por ambiente.
- Rate limiting base en login.
- Auditoria de operaciones criticas.
- Validacion de adjuntos por tipo MIME y tamano.

## Controles pendientes o a reforzar
- Endurecer proteccion CSRF para endpoints mutables con cookies.
- Revisar y endurecer manejo de rutas de adjuntos para evitar traversal.
- Mover bootstrap automatico de datos de seguridad fuera de runtime productivo.
- Definir rotacion operativa de secretos y politica de revocacion de sesiones.

## Reglas operativas
- Ningun secreto real en repositorio ni en ejemplos compartidos.
- En `prod`, cookies `secure=true` y dominio explicito.
- Cada cambio de seguridad debe reflejarse en:
  - `docs/security/*`
  - `contracts/errors/error-catalog.md` si impacta errores
  - pruebas asociadas en `backend/tests`
