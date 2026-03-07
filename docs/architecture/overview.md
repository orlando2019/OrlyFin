# Arquitectura General

## Estilo arquitectonico
Monolito modular por dominios, con backend y frontend separados dentro del mismo repositorio.

## Objetivo tecnico
Escalar por fases sin romper estructura:
- separar reglas de negocio de persistencia y transporte
- versionar API (`/api/v1`)
- soportar multiusuario por organizacion (`organization_id`)

## Mapa de componentes
- `frontend/`: UI y flujos de usuario.
- `backend/`: API, seguridad, reglas y persistencia.
- `contracts/`: fuente de verdad de contratos API y RBAC.
- `docs/`: decisiones y guias operativas.
- `database/`: lineamientos de modelo y seeds.
- `infra/`: runtime local y utilidades de entorno.

## Capas backend por dominio
- `domain`: entidades/constantes de negocio puras.
- `application`: casos de uso y orquestacion.
- `infrastructure`: modelos ORM, repositorios, adaptadores.
- `interfaces`: endpoints HTTP y schemas de transporte.

## Estado actual
- Fases 1-4 con implementacion backend funcional en auth, finanzas base y operaciones.
- Frontend con base modular y pantallas activas en auth y dashboard.
- Existen modulos definidos para fases futuras: `credit_cards`, `reports`, `import_export`.

## Limites de arquitectura
- No microservicios.
- No mezclar logica de negocio en controladores HTTP.
- No acoplar frontend a detalles internos del backend.

## Documentos relacionados
- `docs/architecture/auth-rbac.md`
- `docs/architecture/financial-core-v1.md`
- `docs/architecture/operations-core-v1.md`
- `docs/technical-guidelines.md`
