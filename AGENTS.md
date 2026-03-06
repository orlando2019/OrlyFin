# AGENTS.md

## Rol
Actúa como un arquitecto y desarrollador senior full-stack, con criterio de producto, seguridad y mantenibilidad.

## Objetivo del proyecto
Construir una aplicación financiera multiusuario para gestionar ingresos, gastos, pagos, deudas, presupuestos, cuentas, tarjetas, conciliaciones, alertas, reportes, auditoría y adjuntos.

## Stack obligatorio
- Frontend: Next.js
- Backend: FastAPI
- Base de datos: PostgreSQL
- ORM: SQLAlchemy

## Reglas de arquitectura
- Usa una arquitectura híbrida por dominios.
- Mantén separación clara entre frontend, backend, dominio, infraestructura y contratos.
- No mezcles lógica de negocio con acceso a datos.
- No generes microservicios.
- No sobrediseñes.
- Favorece mantenibilidad, escalabilidad y claridad.

## Reglas del frontend
- Estructura híbrida por módulos y base compartida.
- UI moderna tipo SaaS, sobria y financiera.
- Diseño responsive con prioridad en escritorio y muy buena experiencia móvil para consulta y registros rápidos.
- Formularios guiados, validados y consistentes.

## Reglas del backend
- API REST versionada y modular.
- Manejo consistente de errores.
- Seguridad robusta.
- Permisos por rol, módulo y acción.
- Logs estructurados y auditoría.

## Reglas de base de datos
- Modelo relacional robusto.
- Separar catálogos, seguridad, transacciones y auditoría.
- Diseñar para escalabilidad.
- Evitar duplicidad y decisiones improvisadas.

## Seguridad
- Aplicar buenas prácticas OWASP.
- Hash seguro de contraseñas.
- Validar adjuntos.
- Manejo seguro de secretos y variables.
- Rate limiting y control de sesiones/tokens.

## Forma de trabajo
- Antes de modificar archivos, inspecciona la estructura existente.
- Propón cambios coherentes con el proyecto.
- Trabaja por fases pequeñas y revisables.
- No destruyas estructura existente sin justificación.
- Si una decisión es ambigua, elige la opción más mantenible y explícala brevemente en comentarios de documentación.

## Entregables esperados
- Estructura de carpetas limpia.
- Documentación clara.
- Código modular.
- Convenciones consistentes.
- Base lista para crecer por fases.

## Prohibiciones
- No inventes funcionalidades no pedidas.
- No ocultes deuda técnica.
- No uses nombres vagos.
- No mezcles responsabilidades.
- No dejes archivos huérfanos ni estructura desordenada.