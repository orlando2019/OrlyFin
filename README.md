# OrlyFin

OrlyFin es una aplicacion financiera multiusuario construida como monolito modular por dominios.

## Stack obligatorio
- Frontend: Next.js
- Backend: FastAPI
- Base de datos: PostgreSQL
- ORM: SQLAlchemy

## Estado real del proyecto
- Backend con API v1 activa para auth, RBAC, modulos financieros base y modulos operativos.
- Frontend con base modular y UI funcional en autenticacion y dashboard ejecutivo.
- Contratos y documentacion por fases disponibles en `contracts/` y `docs/`.

## Modulos backend implementados
- `auth_users`, `rbac`
- `accounts`, `income`, `expense`, `debt`, `payment`, `budget`, `dashboard`
- `reconciliation`, `alerts`, `audit`, `attachments`, `settings`

## Modulos planificados (sin implementacion funcional completa)
- `credit_cards`, `reports`, `import_export`

## Estructura del monorepo
- `frontend/`: aplicacion Next.js (App Router) con organizacion por modulos.
- `backend/`: API FastAPI versionada por dominios.
- `contracts/`: OpenAPI, catalogo de errores y matriz RBAC.
- `docs/`: arquitectura, roadmap, operaciones, seguridad y lineamientos tecnicos.
- `database/`: lineamientos de modelo y semillas.
- `infra/`: dockerfiles y scripts de bootstrap.

## Inicio rapido local
1. Copiar variables base:
   - `cp .env.example .env`
2. Verificar variables requeridas:
   - `make check-env`
3. Levantar PostgreSQL:
   - `docker compose up -d postgres`
4. Levantar backend:
   - `make backend-dev`
5. Levantar frontend:
   - `make frontend-dev`

## Credenciales bootstrap local
- Email: `admin@orlyfin.local`
- Password: `ChangeMe123!`

Cambialas antes de usar entornos compartidos.

## Documentacion recomendada para arrancar
- Arquitectura general: `docs/architecture/overview.md`
- Mapa de modulos: `docs/architecture/domain-map.md`
- Roadmap: `docs/roadmap/phases.md`
- Lineamientos tecnicos: `docs/technical-guidelines.md`
- API y contratos: `docs/api/standards.md` y `contracts/openapi/v1/openapi.yaml`
