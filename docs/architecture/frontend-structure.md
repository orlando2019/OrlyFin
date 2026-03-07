# Frontend Structure

Frontend en Next.js (App Router) con estructura hibrida por rutas y modulos.

## Estructura
- `src/app`: rutas, layout global y route groups.
- `src/modules`: logica de presentacion por dominio.
- `src/shared`: configuracion, tipos, utilidades y UI compartida.

## Estado actual
- Implementado:
  - login en `src/modules/auth-users`
  - dashboard ejecutivo en `src/modules/dashboard`
- Base creada (sin UI funcional completa):
  - modulos restantes en `src/modules/*` con README por modulo.

## Convenciones por modulo
Estructura recomendada por modulo frontend:
- `api/`: cliente HTTP del modulo
- `components/`: componentes de interfaz del modulo
- `hooks/`: estado y composicion (cuando aplique)
- `README.md`: alcance y reglas del modulo

## Reglas de implementacion
- Evitar llamadas HTTP directamente desde componentes de pagina.
- Reutilizar tipos compartidos para errores y respuestas comunes.
- Mantener formularios con validacion y mensajes consistentes.
- No mezclar estado global del shell con estado especifico de modulo.
