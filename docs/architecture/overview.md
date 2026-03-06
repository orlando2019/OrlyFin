# Arquitectura General

OrlyFin adopta una arquitectura monolítica modular con enfoque híbrido por dominios.

## Principios
- Separación estricta entre dominio, aplicación, infraestructura e interfaces.
- API REST versionada (`/api/v1`).
- Tenancy por `organization_id`.
- Escalabilidad vertical inicial y desacoplamiento interno para evolución futura.

## Capas
- `domain`: reglas de negocio y modelos puros.
- `application`: casos de uso y orquestación.
- `infrastructure`: persistencia, storage, correo, adaptadores externos.
- `interfaces`: API HTTP, validaciones de entrada/salida, mapeo de errores.

## No objetivos de Fase 1
- No incluir implementación completa de reglas financieras.
- No crear microservicios.

## Referencias Fase 2
- `docs/architecture/auth-rbac.md`
