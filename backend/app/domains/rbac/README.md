# Domain: rbac

## Objetivo
Resolver autorizacion por rol, modulo y accion.

## Alcance Fase 2
- Roles base: `owner_admin`, `admin`, `operator`, `viewer`.
- Permisos base por llave `module:action`.
- Endpoint de consulta de permisos actuales (`/rbac/me/permissions`).
- Asignacion de roles a usuario (`/rbac/users/{user_id}/roles`).

## Capas
- `domain`: catalogo de modulos y acciones.
- `application`: servicios de asignacion y evaluacion de permisos.
- `infrastructure`: modelos/repositorios de roles, permisos y asociaciones.
- `interfaces`: endpoints y dependencias de autorizacion.
