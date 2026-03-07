# Backend Layering

## Objetivo
Mantener separacion clara entre transporte HTTP, reglas de negocio y persistencia.

## Estructura actual
- `app/core`: configuracion, seguridad, errores, logging y dependencias transversales.
- `app/interfaces`: routers versionados y schemas transversales.
- `app/shared`: base SQLAlchemy, storage y utilidades comunes.
- `app/domains/<modulo>`:
  - `domain` (cuando aplica): entidades/constantes de dominio.
  - `application`: casos de uso, servicios y DTOs.
  - `infrastructure`: modelos ORM y repositorios.
  - `interfaces`: endpoints REST por modulo.

## Reglas obligatorias
- Controladores HTTP coordinan entrada/salida, no decisiones de negocio.
- Repositorios encapsulan acceso a datos, no reglas funcionales.
- Validaciones de payload deben vivir en schemas o capa de aplicacion.
- Toda operacion sensible debe auditarse con `trace_id`.

## Estado de implementacion
- El patron por carpetas esta aplicado en modulos implementados.
- Existen casos donde `application` depende directamente de modelos/repos concretos de `infrastructure`.

## Linea de evolucion recomendada
- Reducir acoplamiento de `application` a ORM concreto usando contratos internos por repositorio.
- Mantener migracion gradual sin refactor masivo de una sola vez.
