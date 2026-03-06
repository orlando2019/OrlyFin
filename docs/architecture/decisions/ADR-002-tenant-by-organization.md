# ADR-002: Tenancy por Organización

## Estado
Aceptado.

## Decisión
Todo dato multiusuario debe pertenecer a una `organization_id`.

## Justificación
- Facilita aislamiento lógico de datos.
- Escala para escenarios B2B/B2B2C.
- Permite RBAC consistente por organización.

## Consecuencia
Consultas, índices y auditoría deben incluir `organization_id` cuando aplique.
