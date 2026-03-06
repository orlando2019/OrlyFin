# Auth + RBAC Base (Fase 2)

## Objetivo
Entregar una base funcional de autenticacion, usuarios y permisos por modulo/accion, coherente con la arquitectura por dominios.

## Capas implementadas
- `auth_users`
  - `domain`: entidades de autenticacion.
  - `application`: login, creacion de usuario, emision/validacion de tokens.
  - `infrastructure`: modelos y repositorios de organizaciones/usuarios.
  - `interfaces`: endpoints `/auth/*` y `/users`.
- `rbac`
  - `domain`: modulos/acciones base.
  - `application`: asignacion de roles, resolucion de permisos.
  - `infrastructure`: modelos y repositorios de roles/permisos.
  - `interfaces`: endpoints `/rbac/*` y dependencias de autorizacion.

## Seguridad base aplicada
- Access token corto + refresh token con rotacion en cookies HttpOnly.
- Hash de password con bcrypt via passlib.
- Headers HTTP de seguridad basicos.
- Validacion de permisos por llave `module:action`.

## Bootstrap inicial
Al iniciar backend:
1. Crea tablas de seguridad si no existen.
2. Inserta permisos y roles base.
3. Inserta organizacion y usuario admin bootstrap (entorno local/dev).
