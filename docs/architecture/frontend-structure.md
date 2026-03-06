# Frontend Structure

Frontend con Next.js (App Router), arquitectura híbrida por módulos.

## Distribución
- `src/app`: shell, rutas base y route groups.
- `src/shared`: UI, utilidades, hooks, configuración y tipos comunes.
- `src/modules`: funcionalidades por dominio.

## Reglas
- Componentes compartidos en `shared/ui`.
- Lógica de cada dominio en su módulo correspondiente.
- No acoplar vistas a detalles de infraestructura HTTP.
