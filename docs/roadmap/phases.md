# Roadmap por Fases

Roadmap tecnico orientado a entregables verificables.

## Fase 1 (completada)
Base estructural del monorepo:
- separacion `frontend/` y `backend/`
- contratos base y documentacion inicial
- arranque local y ambientes

## Fase 2 (completada)
Seguridad y acceso:
- auth por cookies HttpOnly (`/auth/*`)
- gestion de usuarios por organizacion
- RBAC por modulo/accion

## Fase 3 (completada en backend)
Core financiero v1:
- cuentas, ingresos, gastos, deudas, pagos, presupuestos
- dashboard ejecutivo con agregados

## Fase 4 (completada en backend)
Core operativo v1:
- conciliaciones, alertas, auditoria, adjuntos, settings

## Fase 5 (en curso pendiente de ejecucion)
Consolidacion y hardening:
- cerrar brechas de seguridad pendientes y reforzar controles
- completar UI de modulos financieros/operativos en frontend
- ampliar pruebas (contrato, integracion, e2e frontend)
- activar modulos planificados: `credit_cards`, `reports`, `import_export`

## Criterio de cierre por fase
Una fase se considera cerrada cuando:
- endpoints y contratos estan alineados
- permisos RBAC del modulo estan definidos
- documentacion del modulo esta actualizada
- pruebas minimas del flujo principal estan presentes
