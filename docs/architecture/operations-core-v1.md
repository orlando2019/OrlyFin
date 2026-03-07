# Operations Core V1 (Fase 4)

Modulos operativos implementados:

- `reconciliation`: conciliacion por cuenta y periodo.
- `alerts`: alertas internas por reglas de negocio.
- `audit`: auditoria estructurada de acciones criticas.
- `attachments`: adjuntos con validacion y almacenamiento desacoplado.
- `settings`: configuracion parametrizable por organizacion.

## Reglas de separacion
- Reconciliacion no altera transacciones; compara saldos y registra estado.
- Alertas consumen datos de negocio, no alteran entidades financieras.
- Auditoria registra trazas, no ejecuta decisiones de negocio.
- Adjuntos solo gestionan metadata/archivo y referencia funcional.
- Settings centraliza parametros y evita hardcode de umbrales.
