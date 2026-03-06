# Financial Core V1

Separacion conceptual implementada en Fase 3:

- `income`: entradas de dinero.
- `expense`: compromisos o salidas esperadas (no descuenta saldo automaticamente).
- `debt`: obligaciones financieras y saldo pendiente.
- `payment`: ejecucion real de pagos (siempre descuenta cuenta; puede impactar deuda/estado de gasto).
- `budget`: planificacion por categoria y periodo.
- `accounts`: contenedores de saldo financiero.
- `dashboard`: agregacion ejecutiva de indicadores.

## Reglas clave
- Crear `income` con cuenta asociada aumenta saldo de cuenta.
- Crear `expense` no disminuye saldo automaticamente.
- Crear `payment` disminuye saldo y puede:
  - marcar gasto como `paid` si referencia un gasto,
  - reducir `balance_amount` de deuda si referencia una deuda.
- Presupuesto consume contra gastos por categoria/periodo.
