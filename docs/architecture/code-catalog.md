# Catalogo Tecnico de Codigo (Repositorio)

## Objetivo y alcance
Este catalogo documenta la estructura tecnica real del repositorio y describe los artefactos mas importantes por carpeta, archivo, clase y funcion relevante.

Criterios aplicados:
- Se priorizan puntos de entrada, logica de negocio, contratos API, seguridad, persistencia, auditoria e integraciones criticas.
- Se listan funciones y clases con impacto funcional directo.
- Archivos de marcador (`__init__.py` vacios, modulos planificados sin implementacion) se agrupan como placeholders.

## 1. Mapa de carpetas del repositorio
- `backend/`: API FastAPI versionada, dominios de negocio, seguridad, persistencia y pruebas.
- `frontend/`: aplicacion Next.js (App Router), modulos UI y clientes API.
- `contracts/`: contratos funcionales (OpenAPI, matriz RBAC, catalogo de errores).
- `database/`: lineamientos de modelo relacional y semillas.
- `docs/`: arquitectura, seguridad, operaciones y guias tecnicas.
- `infra/`: scripts de bootstrap/verificacion y Dockerfiles.

## 2. Backend

### 2.1 Punto de entrada y capa core

#### `backend/app/main.py`
- `lifespan`: inicializa esquema (opcional por entorno) y bootstrap de seguridad/datos base.
- `trace_middleware`: inyecta `trace_id`, mide latencia y registra log estructurado por request.
- `security_headers_middleware`: agrega cabeceras de endurecimiento (`CSP`, `X-Frame-Options`, etc.).
- `app_error_handler`: normaliza `AppError` al contrato de error de la API.
- `validation_exception_handler`: transforma errores de validacion FastAPI al mismo modelo de error.
- `unhandled_exception_handler`: respuesta consistente para excepciones no controladas.

#### `backend/app/core/config.py`
- `Settings`: contrato central de configuracion por variables de entorno.
- `parse_cors_origins`: parsea lista CORS desde string CSV o lista.
- `parse_attachment_allowed_mime_types`: parsea MIME types permitidos para adjuntos.
- `get_settings`: cachea una sola instancia de configuracion para toda la app.

#### `backend/app/core/security.py`
- `JwtCookiePolicy`: politica de cookies JWT (duraciones y flags de seguridad).
- `hash_password`: hashing PBKDF2-SHA256 con salt aleatorio.
- `verify_password`: validacion segura de password usando comparacion constante.
- `_build_token_payload`: construye claims base JWT (`sub`, `type`, `iat`, `exp`).
- `create_access_token`: emite token de acceso.
- `create_refresh_token`: emite token de refresco.
- `decode_access_token` / `decode_refresh_token`: valida y decodifica JWT segun secreto/tipo.

#### `backend/app/core/errors.py`
- `ErrorDetail`: detalle de error por campo.
- `ErrorResponse`: contrato uniforme de respuesta de error.
- `AppError`: excepcion de dominio/aplicacion con `code` y `status_code`.
- `build_error_response`: fabrica errores con `trace_id` y timestamp UTC.

#### `backend/app/core/dependencies.py`
- `get_trace_id`: expone `trace_id` desde estado del request.
- `get_db`: ciclo de vida de sesion SQLAlchemy por request.

#### `backend/app/core/logging.py`
- `JsonFormatter`: serializa logs estructurados JSON con campos extra.
- `configure_logging`: inicializa logging raiz una sola vez.
- `get_logger`: obtiene logger garantizando configuracion previa.

#### `backend/app/core/rate_limit.py`
- `limit_requests`: dependencia FastAPI para rate limiting in-memory por IP/ventana.

### 2.2 Interfaces API comunes

#### `backend/app/interfaces/api/v1/router.py`
- Enrutador agregador de todos los modulos REST v1.

#### `backend/app/interfaces/api/v1/health.py`
- `health_check`: endpoint de salud de backend.

#### `backend/app/interfaces/schemas/common.py`
- `HealthResponse`: contrato de salida para health check.

#### `backend/app/interfaces/schemas/error.py`
- `ErrorResponseSchema`: contrato de error publico.

### 2.3 Shared (cross-cutting)

#### `backend/app/shared/domain/value_objects.py`
- `Money`: value object inmutable, valida monto no negativo y moneda ISO-4217 alpha-3.

#### `backend/app/shared/domain/events.py`
- `DomainEvent`: evento de dominio con timestamp UTC.

#### `backend/app/shared/application/unit_of_work.py`
- `UnitOfWork`: contrato abstracto de `commit`/`rollback`.

#### `backend/app/shared/infrastructure/db/base.py`
- `Base`: clase base declarativa SQLAlchemy.

#### `backend/app/shared/infrastructure/db/session.py`
- `engine`: motor SQLAlchemy configurado por entorno.
- `SessionLocal`: factory de sesiones transaccionales.

#### `backend/app/shared/infrastructure/db/models/audit_base.py`
- `AuditBaseMixin`: campos comunes (`id`, `created_at`, `updated_at`).

#### `backend/app/shared/infrastructure/db/models/tenant_base.py`
- `TenantBaseMixin`: campo comun `organization_id` para multi-tenant.

#### `backend/app/shared/infrastructure/db/model_registry.py`
- Registro explicito de modelos ORM para construir metadata/migraciones.

#### `backend/app/shared/infrastructure/storage/interface.py`
- `StorageProvider`: contrato de almacenamiento (`save`, `delete`).

#### `backend/app/shared/infrastructure/storage/local_provider.py`
- `LocalStorageProvider`: provider local con validacion anti path traversal.
- `_safe_target`: valida que la ruta efectiva quede bajo `base_path`.
- `save`: persiste bytes en disco local.
- `delete`: elimina recurso si existe.

### 2.4 Dominios implementados

#### `accounts`
Archivos:
- `interfaces/api.py`
  - `create_account`: crea cuenta validando permisos RBAC.
  - `list_accounts`: lista cuentas por organizacion.
- `application/schemas.py`
  - `AccountCreateRequest`, `AccountResponse`, `AccountListResponse`.
- `application/service.py`
  - `AccountsService.create_account`: valida tipo/saldo inicial, evita nombre duplicado por organizacion, registra auditoria.
  - `AccountsService.list_accounts`: consulta cuentas.
  - `to_account_response`: mapea ORM -> DTO.
  - `get_accounts_service`: factory DI.
- `infrastructure/models.py`
  - `FinancialAccount`: entidad de cuenta financiera y saldo actual.
- `infrastructure/repository.py`
  - `get_by_id_for_org`, `get_by_name_for_org`, `create`, `list_for_org`, `sum_balances_for_org`.

#### `auth_users`
Archivos:
- `interfaces/api.py`
  - `_set_auth_cookies`: aplica cookies HttpOnly de acceso/refresco.
  - `_clear_auth_cookies`: invalida cookies de sesion.
  - `login`: autentica y emite cookies+perfil.
  - `refresh_token`: rota par de tokens con refresh cookie.
  - `logout`: cierra sesion por limpieza de cookies.
  - `me`: devuelve perfil y autorizaciones efectivas.
  - `create_user`: alta de usuario con roles, protegida por permiso.
- `interfaces/schemas.py`
  - `AuthMessageResponse`, `MeResponse`.
- `application/schemas.py`
  - `LoginRequest`, `UserCreateRequest`, `AuthUserResponse`.
- `application/service.py`
  - `AuthUsersService.ensure_bootstrap_data`: crea organizacion/admin inicial si no existe.
  - `AuthUsersService.authenticate`: valida credenciales y estado de usuario.
  - `AuthUsersService.issue_token_pair`: genera access+refresh.
  - `AuthUsersService.decode_and_get_user`: valida JWT tipo/subject y carga usuario.
  - `AuthUsersService.create_user`: crea usuario y asigna roles.
  - `get_auth_users_service`: factory DI.
  - `get_current_user`: extrae usuario autenticado desde cookie de acceso.
- `domain/entities.py`
  - `AuthenticatedUser`: representacion inmutable de usuario autenticado.
- `infrastructure/models.py`
  - `Organization`, `User`.
- `infrastructure/repository.py`
  - `OrganizationRepository.get_by_slug/create`.
  - `UserRepository.get_by_id/get_by_email/create`.

#### `rbac`
Archivos:
- `interfaces/api.py`
  - `my_permissions`: retorna permisos efectivos del usuario actual.
  - `assign_roles`: asigna roles a usuario bajo control RBAC.
- `interfaces/dependencies.py`
  - `get_rbac_service`: factory DI.
  - `require_permission`: dependency guard `module:action`.
- `interfaces/schemas.py`
  - `PermissionListResponse`, `AssignRoleRequest`, `AssignRoleResponse`.
- `application/service.py`
  - `RbacService.ensure_default_permissions_and_roles`: bootstrap de catalogo RBAC y mapeos rol-permiso.
  - `assign_roles_to_user`: asigna roles evitando cruce de organizacion.
  - `get_user_roles`: consulta roles efectivos.
  - `get_user_permission_keys`: consulta llaves `module:action`.
  - `has_permission`: evaluador booleano.
- `domain/constants.py`
  - `MODULES`, `ACTIONS`: catalogos canonicos RBAC.
- `infrastructure/models.py`
  - `Role`, `Permission`, `UserRole`, `RolePermission`.
- `infrastructure/repository.py`
  - Repositorios CRUD/minimos para rol, permiso y relaciones.

#### `income`
Archivos:
- `interfaces/api.py`: `create_income`, `list_incomes`.
- `application/schemas.py`: `IncomeCreateRequest`, `IncomeResponse`, `IncomeListResponse`.
- `application/service.py`
  - `IncomeService.create_income`: valida monto/tipo, crea registro y suma saldo si hay cuenta.
  - `IncomeService.list_incomes`.
  - `to_income_response`, `get_income_service`.
- `infrastructure/models.py`: `IncomeRecord`.
- `infrastructure/repository.py`
  - `create`, `list_for_org`, `sum_for_period`.

#### `expense`
Archivos:
- `interfaces/api.py`: `create_expense`, `list_expenses`.
- `application/schemas.py`: `ExpenseCreateRequest`, `ExpenseResponse`, `ExpenseListResponse`.
- `application/service.py`
  - `ExpenseService.create_expense`: valida monto/tipo/cuenta y crea en estado `pending`.
  - `ExpenseService.list_expenses`.
  - `to_expense_response`, `get_expense_service`.
- `infrastructure/models.py`: `ExpenseRecord`.
- `infrastructure/repository.py`
  - `create`, `get_by_id_for_org`, `list_for_org`, `sum_for_period`, `sum_by_category_period`, `count_pending`.

#### `debt`
Archivos:
- `interfaces/api.py`: `create_debt`, `list_debts`.
- `application/schemas.py`: `DebtCreateRequest`, `DebtResponse`, `DebtListResponse`.
- `application/service.py`
  - `DebtService.create_debt`: valida principal/tipo/cuotas y crea deuda activa.
  - `DebtService.list_debts`.
  - `to_debt_response`, `get_debt_service`.
- `infrastructure/models.py`: `DebtRecord`.
- `infrastructure/repository.py`
  - `create`, `get_by_id_for_org`, `list_for_org`, `sum_outstanding`, `count_active`.

#### `payment`
Archivos:
- `interfaces/api.py`: `create_payment`, `list_payments`.
- `application/schemas.py`: `PaymentCreateRequest`, `PaymentResponse`, `PaymentListResponse`.
- `application/service.py`
  - `PaymentService.create_payment`: valida tipo/referencia, descuenta cuenta y sincroniza estados de gasto/deuda.
  - `PaymentService.list_payments`.
  - `to_payment_response`, `get_payment_service`.
- `infrastructure/models.py`: `PaymentRecord`.
- `infrastructure/repository.py`
  - `create`, `list_for_org`, `sum_for_period`.

#### `budget`
Archivos:
- `interfaces/api.py`: `create_budget`, `list_budgets`.
- `application/schemas.py`: `BudgetCreateRequest`, `BudgetResponse`, `BudgetListResponse`.
- `application/service.py`
  - `BudgetService.create_budget`: valida rangos y umbral, crea presupuesto.
  - `BudgetService.list_budgets`.
  - `BudgetService.to_budget_response`: calcula consumo/uso y bandera de umbral.
  - `get_budget_service`.
- `infrastructure/models.py`: `BudgetRecord`.
- `infrastructure/repository.py`
  - `create`, `list_for_org`, `sum_planned_for_overlap`.

#### `dashboard`
Archivos:
- `interfaces/api.py`: `get_executive_dashboard`.
- `application/schemas.py`: `ExecutiveDashboardResponse`.
- `application/service.py`
  - `DashboardService.get_executive_summary`: agrega KPIs financieros/operativos del periodo.
  - `get_dashboard_service`.

#### `reconciliation`
Archivos:
- `interfaces/api.py`: `create_reconciliation`, `list_reconciliations`, `resolve_reconciliation`.
- `application/schemas.py`: `ReconciliationCreateRequest`, `ReconciliationResolveRequest`, `ReconciliationResponse`, `ReconciliationListResponse`.
- `application/service.py`
  - `ReconciliationService.create_reconciliation`: compara libro vs extracto y clasifica estado.
  - `ReconciliationService.resolve_reconciliation`: cierra diferencia con trazabilidad.
  - `ReconciliationService.list_reconciliations`.
  - `to_reconciliation_response`, `get_reconciliation_service`.
- `infrastructure/models.py`: `ReconciliationRecord`.
- `infrastructure/repository.py`
  - `create`, `get_by_id_for_org`, `list_for_org`.

#### `alerts`
Archivos:
- `interfaces/api.py`: `evaluate_alerts`, `list_alerts`, `mark_alert_read`.
- `application/schemas.py`: `AlertResponse`, `AlertListResponse`, `EvaluateAlertsResponse`.
- `application/service.py`
  - `AlertsService._build_budget_alerts`: alerta por umbral de presupuesto.
  - `AlertsService._build_debt_alerts`: alerta por deuda proxima a vencimiento.
  - `AlertsService.evaluate_alerts`: ejecuta reglas y genera auditoria.
  - `AlertsService.list_alerts`.
  - `AlertsService.mark_read`: marca alerta como leida.
  - `to_alert_response`, `get_alerts_service`.
- `infrastructure/models.py`: `AlertRecord`.
- `infrastructure/repository.py`
  - `get_open_by_fingerprint`, `create`, `get_by_id_for_org`, `list_for_org`.

#### `audit`
Archivos:
- `interfaces/api.py`: `list_audit_events`.
- `application/schemas.py`: `AuditEventResponse`, `AuditEventListResponse`.
- `application/service.py`
  - `AuditService.record_event`: serializa detalles y registra evento.
  - `AuditService.list_events`: consulta con filtros y limites.
  - `to_audit_event_response`, `get_audit_service`.
- `infrastructure/models.py`: `AuditEvent`.
- `infrastructure/repository.py`
  - `create`, `list_for_org`.

#### `attachments`
Archivos:
- `interfaces/api.py`: `upload_attachment`, `delete_attachment`, `list_attachments`.
- `application/schemas.py`: `AttachmentResponse`, `AttachmentListResponse`.
- `application/service.py`
  - `AttachmentsService._safe_name`: sanitiza nombre de archivo.
  - `AttachmentsService._validate_file`: valida MIME y tamano maximo.
  - `AttachmentsService._safe_segment`: sanea segmentos de ruta (`module`, `entity_id`).
  - `AttachmentsService.upload_attachment`: valida, guarda en storage, persiste metadata y audita.
  - `AttachmentsService.delete_attachment`: elimina archivo fisico y marca estado `deleted`.
  - `AttachmentsService.list_attachments`.
  - `to_attachment_response`, `get_attachments_service`.
- `infrastructure/models.py`: `AttachmentRecord`.
- `infrastructure/repository.py`
  - `create`, `get_by_id_for_org`, `list_for_org`.

#### `settings`
Archivos:
- `interfaces/api.py`: `upsert_setting`, `list_settings`, `get_setting`.
- `application/schemas.py`: `SettingUpsertRequest`, `SettingResponse`, `SettingListResponse`.
- `application/service.py`
  - `SettingsService._serialize`: serializa valores por tipo (`string`, `int`, `float`, `bool`, `json`).
  - `SettingsService._deserialize`: reconstruye tipo de valor no sensible.
  - `SettingsService.upsert_setting`: crea/actualiza parametro y audita.
  - `SettingsService.get_setting`, `SettingsService.list_settings`.
  - `SettingsService.to_response`: protege valores sensibles.
  - `get_settings_service`.
- `infrastructure/models.py`: `SystemSetting`.
- `infrastructure/repository.py`
  - `get_by_key`, `upsert`, `list_for_org`.

### 2.5 Dominios placeholders
- `credit_cards`, `reports`, `import_export`: solo estructura inicial y README funcional, sin clases/servicios/endpoints activos en backend.

### 2.6 Migraciones y ciclo de esquema

#### `backend/migrations/env.py`
- Configura Alembic en modo offline/online usando `settings.database_url`.

#### `backend/migrations/versions/20260305_0001_auth_rbac_base.py`
- Crea tablas base de seguridad: `organizations`, `users`, `roles`, `permissions`, `user_roles`, `role_permissions`.

#### `backend/migrations/versions/20260306_0002_financial_core_v1.py`
- Crea modulos financieros core: `financial_accounts`, `income_records`, `expense_records`, `debt_records`, `payment_records`, `budget_records`.

#### `backend/migrations/versions/20260306_0003_ops_modules_v1.py`
- Crea modulos operativos v1: `audit_events`, `system_settings`, `attachment_records`, `alert_records`, `reconciliation_records`.

### 2.7 Pruebas backend

#### `backend/tests/conftest.py`
- Ajusta `sys.path` para ejecucion de tests sobre paquete backend.

#### `backend/tests/unit/test_health.py`
- `test_health_check`: verifica endpoint de salud y contrato base.

#### `backend/tests/unit/test_auth_and_rbac.py`
- `test_login_and_me`: valida flujo de login + perfil autenticado.
- `test_create_user_requires_permission_and_creates_user`: valida alta de usuario con roles.

#### `backend/tests/unit/test_financial_modules.py`
- `_login`: helper de autenticacion para pruebas.
- `test_financial_modules_v1_flow`: prueba integrada de cuentas, ingresos, gastos, deudas, pagos, presupuestos y dashboard.

#### `backend/tests/unit/test_phase4_operations_modules.py`
- `_login`: helper de autenticacion.
- `test_phase4_modules_flow`: prueba integrada de alertas, settings, adjuntos, conciliaciones y auditoria.

#### `backend/tests/unit/test_storage_security.py`
- `test_local_storage_rejects_path_traversal`: valida bloqueo de rutas peligrosas.
- `test_local_storage_accepts_safe_relative_path`: valida rutas relativas seguras.

## 3. Frontend

### 3.1 App Router y layout

#### `frontend/src/app/layout.tsx`
- `RootLayout`: shell global (header, contenedor principal y metadata).

#### `frontend/src/app/page.tsx`
- `HomePage`: landing tecnica con accesos a dashboard y login.

#### `frontend/src/app/(auth)/signin/page.tsx`
- `SignInPage`: pagina de autenticacion que delega en `SignInForm`.

#### `frontend/src/app/(dashboard)/dashboard/page.tsx`
- `DashboardPage`: pagina de dashboard que delega en `ExecutiveDashboardPanel`.

#### `frontend/src/app/api/health/route.ts`
- `GET`: health endpoint de frontend (estado/version/timestamp).

#### `frontend/src/app/globals.css`
- Define tokens visuales, layout shell, formularios, tarjetas y responsive base.

### 3.2 Modulos frontend implementados con codigo

#### `frontend/src/modules/auth-users/api/client.ts`
- `login`: consume `POST /auth/login` con cookies.
- `me`: consume `GET /auth/me` para perfil actual.
- Tipos: `LoginPayload`, `MeResponse`.

#### `frontend/src/modules/auth-users/components/signin-form.tsx`
- `SignInForm`: formulario controlado de login, manejo de estados (`loading`, `error`, `session`) y lectura de perfil tras autenticacion.

#### `frontend/src/modules/dashboard/api/client.ts`
- `getExecutiveDashboard`: consume `GET /dashboard/executive`.
- Tipo: `ExecutiveDashboard`.

#### `frontend/src/modules/dashboard/components/executive-dashboard.tsx`
- `money`: helper de formato monetario.
- `ExecutiveDashboardPanel`: carga asyncrona de KPI, manejo de estados y render de metricas.

### 3.3 Shared frontend

#### `frontend/src/shared/config/env.ts`
- `env.apiBaseUrl`: base URL configurable para API backend v1.

#### `frontend/src/shared/types/api.ts`
- `ErrorResponse`: contrato generico de errores API.

### 3.4 Modulos frontend placeholders
- `accounts`, `alerts`, `attachments`, `audit`, `budget`, `credit-cards`, `debt`, `expense`, `import-export`, `income`, `payment`, `rbac`, `reconciliation`, `reports`, `settings`: contienen README de intencion y estructura, sin implementacion funcional de componentes/cliente aun.

## 4. Contratos, BD documental e infraestructura

### 4.1 Contratos (`contracts/`)
- `contracts/openapi/v1/openapi.yaml`: contrato API v1 para integracion.
- `contracts/rbac/permissions-matrix.md`: matriz de permisos por modulo/accion.
- `contracts/errors/error-catalog.md`: catalogo de codigos de error.

### 4.2 Base de datos documental (`database/`)
- `database/model/domains-overview.md`: segmentacion de dominio del modelo.
- `database/model/core-entities.md`: entidades troncales y relaciones.
- `database/model/naming-conventions.md`: convenciones de nomenclatura.
- `database/seeds/README.md`: lineamientos de datos semilla.

### 4.3 Infraestructura (`infra/`)
- `infra/scripts/check-env.sh`: verifica variables minimas obligatorias.
- `infra/scripts/bootstrap.sh`: automatiza chequeo e instalacion local backend/frontend.
- `infra/docker/backend.Dockerfile`: imagen de API backend.
- `infra/docker/frontend.Dockerfile`: imagen de app frontend.

## 5. Archivos de soporte del proyecto
- `README.md`: estado general, stack, modulos y arranque local.
- `backend/README.md`: alcance backend por fases y endpoints disponibles.
- `frontend/README.md`: alcance frontend por fases.
- `docs/README.md`: indice de documentacion.
- `AGENTS.md`: lineamientos de arquitectura, seguridad y forma de trabajo para agentes.
- `backend/pyproject.toml`: dependencias Python y tooling del backend.
- `backend/alembic.ini`: configuracion base de Alembic.
- `frontend/package.json`: dependencias y scripts de build/dev frontend.
- `frontend/next.config.ts`: configuracion de runtime/build de Next.js.
- `frontend/tsconfig.json`: configuracion TypeScript y aliases.
- `Makefile`: comandos de desarrollo y operacion local.
- `docker-compose.yml`: servicios base de infraestructura local.

## 6. Notas de mantenibilidad
- El backend sigue una separacion por capas consistente (interfaces/application/infrastructure) en dominios implementados.
- Hay dominios reservados con scaffolding pero sin logica funcional; esto evita sobre-diseno prematuro y mantiene expansion ordenada por fases.
- La auditoria ya se encuentra integrada transversalmente en casos de uso criticos (creacion, evaluacion, cambios de estado).
