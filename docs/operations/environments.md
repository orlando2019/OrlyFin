# Ambientes

Ambientes soportados:
- `local`
- `dev`
- `qa`
- `prod`

## Objetivo por ambiente
- `local`: desarrollo en maquina del equipo.
- `dev`: integracion continua y pruebas de modulo.
- `qa`: validacion funcional previa a release.
- `prod`: operacion real.

## Diferencias minimas obligatorias
- Conexion a base de datos por ambiente.
- Politica de CORS por ambiente.
- Politica de cookies (`secure`, `samesite`, `domain`) por ambiente.
- Nivel de logging por ambiente.
- Secretos propios por ambiente.
- Flags de arranque controlado (`DB_AUTO_CREATE_SCHEMA`, `BOOTSTRAP_SECURITY_DATA`) segun ambiente.

## Archivos de referencia
- `.env.example`: plantilla base.
- `.env.local.example`, `.env.dev.example`, `.env.qa.example`, `.env.prod.example`: ejemplos por entorno.

## Regla de despliegue
- No desplegar usando valores default de secretos.
- Validar variables con `make check-env` antes de arrancar.
- Migraciones de esquema deben ejecutarse de forma controlada por pipeline/operacion.
- En `qa/prod`, mantener `DB_AUTO_CREATE_SCHEMA=false` y `BOOTSTRAP_SECURITY_DATA=false`.
