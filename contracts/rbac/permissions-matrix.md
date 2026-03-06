# Matriz RBAC Inicial

## Roles iniciales
- `owner_admin`
- `admin`
- `operator`
- `viewer`

## Acciones estándar
- `read`
- `create`
- `update`
- `delete`
- `approve`
- `export`

## Módulos
- auth_users
- rbac
- dashboard
- income
- expense
- debt
- payment
- budget
- accounts
- credit_cards
- reconciliation
- alerts
- reports
- audit
- attachments
- settings
- import_export

## Política base
- `owner_admin`: acceso total.
- `admin`: acceso casi total sin acciones superadministrativas.
- `operator`: operación diaria sobre módulos asignados.
- `viewer`: solo consulta.
