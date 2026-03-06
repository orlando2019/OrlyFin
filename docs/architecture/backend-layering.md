# Backend Layering

## Regla de separación
- Controladores HTTP no contienen lógica de negocio.
- Repositorios no toman decisiones de negocio.
- Casos de uso dependen de interfaces, no de frameworks concretos.

## Estructura base
- `app/core`: configuración transversal.
- `app/interfaces`: capa REST y schemas.
- `app/shared`: componentes compartidos.
- `app/domains`: módulos de negocio por dominio.

## Convenciones
- Entradas/salidas validadas con Pydantic.
- Errores de negocio mapeados a catálogo de errores.
- Logging estructurado con `trace_id`.
