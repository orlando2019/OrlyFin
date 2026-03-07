# Mapa de Modulos y Dominios

Este mapa distingue estado real por modulo para evitar ambiguedades de alcance.

## Backend
| Modulo | Responsabilidad principal | Estado |
| --- | --- | --- |
| `auth_users` | autenticacion, perfil y usuarios por organizacion | implementado |
| `rbac` | permisos por `module:action` y asignacion de roles | implementado |
| `accounts` | cuentas financieras y saldo actual | implementado |
| `income` | registro de ingresos y aumento de saldo de cuenta | implementado |
| `expense` | registro de gastos con estado (`pending`/`paid`) | implementado |
| `debt` | deudas y saldo pendiente | implementado |
| `payment` | pagos que descuentan cuenta e impactan gasto/deuda | implementado |
| `budget` | presupuestos por categoria y periodo | implementado |
| `dashboard` | agregados ejecutivos financieros | implementado |
| `reconciliation` | conciliaciones por cuenta y periodo | implementado |
| `alerts` | generacion y consulta de alertas operativas | implementado |
| `audit` | eventos de auditoria consultables | implementado |
| `attachments` | carga/listado/borrado logico de adjuntos | implementado |
| `settings` | configuracion parametrizable por organizacion | implementado |
| `credit_cards` | manejo de tarjetas de credito | planificado |
| `reports` | reportes avanzados y exportables | planificado |
| `import_export` | importacion/exportacion de datos | planificado |

## Frontend
| Modulo | Alcance UI actual | Estado |
| --- | --- | --- |
| `auth-users` | login y consulta de sesion (`/signin`) | implementado |
| `dashboard` | panel ejecutivo base (`/dashboard`) | implementado |
| resto de modulos (`accounts`, `income`, `expense`, `debt`, `payment`, `budget`, `reconciliation`, `alerts`, `audit`, `attachments`, `settings`, `credit-cards`, `reports`, `import-export`, `rbac`) | estructura y README por modulo | base creada |

## Regla de crecimiento
Cada modulo nuevo debe nacer con:
- endpoint y schema en backend
- entrada en OpenAPI (`contracts/openapi/v1/openapi.yaml`)
- permiso RBAC en matriz y seed
- README de modulo backend y frontend
