# OrlyFin

OrlyFin es una aplicación financiera multiusuario con arquitectura monolítica modular por dominios.

## Stack
- Frontend: Next.js
- Backend: FastAPI
- Base de datos: PostgreSQL
- ORM: SQLAlchemy

## Objetivo de esta fase (Fase 1)
- Base profesional de monorepo.
- Arquitectura híbrida por dominios definida.
- Backend y frontend arrancables con entrypoints mínimos.
- Contratos, documentación, ambientes y seguridad base.

## Estado actual (Fase 2)
- Base de autenticación implementada (`/api/v1/auth/*`).
- Usuarios con organización y hash seguro de contraseña.
- RBAC por módulo/acción con roles iniciales (`owner_admin`, `admin`, `operator`, `viewer`).
- Bootstrap local de organización, permisos y usuario administrador.

## Estructura principal
- `frontend/`: aplicación web Next.js por módulos.
- `backend/`: API FastAPI versionada y modular.
- `contracts/`: OpenAPI, errores y RBAC.
- `docs/`: arquitectura, seguridad, operaciones y roadmap.
- `database/`: lineamientos de modelo y semillas.
- `infra/`: Dockerfiles y scripts operativos.

## Inicio rápido
1. Copia variables de entorno:
   - `cp .env.example .env`
2. Verifica entorno:
   - `make check-env`
3. Levanta dependencias:
   - `docker compose up -d postgres`
4. Backend:
   - `make backend-dev`
5. Frontend:
   - `make frontend-dev`

## Credenciales bootstrap local
- Email: `admin@orlyfin.local`
- Password: `ChangeMe123!`

Se recomienda cambiarlas en `.env` antes de usar entornos compartidos.

## Estado
Esta base no incluye todavía lógica de negocio de módulos financieros. Se implementará por fases incrementales.
