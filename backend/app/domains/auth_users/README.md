# Domain: auth_users

## Objetivo
Gestionar autenticacion y ciclo base de usuarios por organizacion.

## Alcance Fase 2
- Login con cookies HttpOnly (access + refresh).
- Perfil de usuario autenticado (`/auth/me`).
- Creacion de usuarios con control de permisos (`/users`).
- Bootstrap de organizacion y usuario admin local.

## Capas
- `domain`: entidad autenticada.
- `application`: servicios de autenticacion y gestion de usuario.
- `infrastructure`: modelos/repositorios de organizacion y usuario.
- `interfaces`: endpoints REST y schemas.
