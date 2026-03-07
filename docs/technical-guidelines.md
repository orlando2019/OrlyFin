# Lineamientos Tecnicos

Guia breve para mantener coherencia tecnica del proyecto en nuevas fases.

## 1) Arquitectura y estructura
- Mantener separacion `frontend/` y `backend/`.
- En backend, respetar capas por dominio: `application`, `infrastructure`, `interfaces` y `domain` cuando aplique.
- No mezclar logica de negocio en routers HTTP.
- No crear microservicios para resolver problemas de organizacion interna.

## 2) API y contratos
- Toda ruta publica bajo `/api/v1`.
- Todo endpoint nuevo o cambio de schema debe reflejarse en `contracts/openapi/v1/openapi.yaml`.
- Mantener errores alineados con `contracts/errors/error-catalog.md`.
- Proteger endpoints por permisos `module:action` cuando no sean publicos.

## 3) Frontend
- Todo flujo nuevo vive en su modulo dentro de `frontend/src/modules`.
- Evitar fetch directo desde paginas; encapsular en `modules/<modulo>/api`.
- Reutilizar tipos y configuracion de `frontend/src/shared`.
- Mantener formularios consistentes en validacion, mensajes y estados de carga.

## 4) Base de datos y persistencia
- Cambios de esquema siempre por migraciones (`backend/migrations`).
- Evitar duplicidad de entidades o campos sin justificacion funcional.
- Mantener `organization_id` en entidades multiusuario que apliquen.
- Actualizar `database/model/*` si cambia el modelo conceptual.

## 5) Seguridad minima
- Secretos por entorno, nunca hardcodeados.
- Auth en cookies con configuracion segura por ambiente.
- Validar tamano/tipo de adjuntos y reforzar controles de ruta.
- Auditar operaciones criticas con `trace_id`.

## 6) Pruebas y calidad
- Backend: cubrir flujo principal de cada modulo nuevo.
- Frontend: agregar pruebas unitarias/e2e de los flujos activos.
- Contrato: validar que OpenAPI represente lo expuesto por la API.
- No cerrar una fase sin pruebas minimas del camino feliz y errores clave.

## 7) Documentacion obligatoria por cambio relevante
- Actualizar README principal si cambia alcance general.
- Actualizar docs del modulo afectado.
- Actualizar roadmap si cambia el orden de fases.
- Registrar decisiones estructurales en `docs/architecture/decisions/`.
