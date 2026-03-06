# Matriz RBAC Inicial (Fase 2)

## Roles
- `owner_admin`: control total de modulos y acciones.
- `admin`: gestion administrativa sobre operacion, sin privilegios de owner.
- `operator`: operacion diaria en modulos transaccionales.
- `viewer`: lectura.

## Acciones por modulo
Acciones base: `read`, `create`, `update`, `delete`, `approve`, `export`.

## Asignacion por rol
- `owner_admin`: todos los modulos x todas las acciones.
- `admin`: todos los modulos x (`read`, `create`, `update`, `delete`, `export`).
- `operator`: `income`, `expense`, `debt`, `payment`, `budget`, `accounts`, `credit_cards` x (`read`, `create`, `update`).
- `viewer`: todos los modulos x `read`.

## Regla tecnica
- En runtime se valida permiso como llave `module:action`.
- El endpoint protegido responde `403 FORBIDDEN` cuando no exista permiso.
