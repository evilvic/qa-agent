# Decision Log

Registro de decisiones del proyecto. Cada decisión tiene contexto, opciones consideradas, resultado y si es reversible.

---

## D-001: Producto app-agnostic, no atado a una app específica

- **Fecha:** 2026-02-21
- **Contexto:** El PoC original se construyó para probar una app específica (minu). El producto debe funcionar con cualquier web app.
- **Decisión:** Eliminar toda referencia hardcoded a apps específicas. El modelo de datos incluye "Projects" donde el usuario configura su app target.
- **Reversible:** Sí
- **Estado:** Aprobada

## D-002: SQLite como base de datos del MVP

- **Fecha:** 2026-02-21
- **Contexto:** Se necesita persistencia para test cases, runs y memories. Opciones: SQLite, PostgreSQL, archivos JSON.
- **Opciones:**
  - SQLite: Zero config, file-based, suficiente para un usuario. Migrar después si es necesario.
  - PostgreSQL: Más robusto, pero requiere setup y es overkill para MVP de un usuario.
  - JSON files: Frágil, no soporta queries, no escala.
- **Decisión:** SQLite. Migrar a PostgreSQL cuando haya multi-tenant.
- **Reversible:** Sí (SQLModel abstrae el engine)
- **Estado:** Aprobada

## D-003: Memoria del agente via prompt injection, no Playwright script replay

- **Fecha:** 2026-02-21
- **Contexto:** El agente necesita reutilizar conocimiento de runs anteriores. Dos approaches: (A) guardar el execution path y pasarlo como contexto en el prompt, (B) grabar un Playwright script y re-ejecutarlo directamente.
- **Opciones:**
  - A) Prompt injection: Flexible, resiliente a cambios menores en UI, usa el mismo pipeline.
  - B) Script replay: Más rápido y barato (no usa LLM), pero frágil ante cualquier cambio de selectores/layout.
- **Decisión:** Prompt injection (opción A). El agente recibe el path anterior como contexto y decide si seguirlo o explorar. Más resiliente.
- **Reversible:** Sí
- **Estado:** Aprobada

## D-004: Pass/fail evaluado por el LLM, no por assertions hardcoded

- **Fecha:** 2026-02-21
- **Contexto:** Los test cases necesitan un veredicto. Opciones: assertions tipo Cypress (exactas, frágiles) o evaluación semántica por el LLM (flexible, más costosa).
- **Decisión:** LLM evalúa pass/fail basado en expected_outcome en lenguaje natural. Es el diferenciador vs herramientas tradicionales.
- **Reversible:** Sí
- **Estado:** Aprobada

## D-005: Model routing por contexto

- **Fecha:** 2026-02-21
- **Contexto:** Cada run cuesta tokens de OpenAI. Cuando hay memoria de un run exitoso anterior, no se necesita el modelo más caro.
- **Decisión:** Usar modelo barato (gpt-4.1-mini o nano) cuando hay memory disponible. Escalar a modelo más capaz cuando es primera ejecución o cuando el replay falla.
- **Reversible:** Sí
- **Estado:** Aprobada, implementar en Fase 2

## D-006: Frontend iterativo, no reescritura

- **Fecha:** 2026-02-21
- **Contexto:** El frontend actual es un monolito (App.vue). Opciones: refactorizar en componentes desde el inicio, o iterar sobre el monolito agregando features.
- **Decisión:** Iterar. Dividir en componentes cuando la complejidad lo requiera, no antes. El monolito funciona para el MVP.
- **Reversible:** Sí
- **Estado:** Aprobada

## D-007: Experiencia guía infraestructura, no al revés

- **Fecha:** 2026-02-21
- **Contexto:** El plan original proponía construir backend (modelo de datos, endpoints) primero y UI después. El owner corrigió: la experiencia debe definirse primero para que el modelo de datos y la API sirvan a la experiencia, no al revés.
- **Decisión:** Invocar Experience Architect antes de implementar. El sistema de experiencia (journeys, estados, componentes) valida y ajusta el modelo de datos y la API.
- **Reversible:** N/A (es un principio de proceso)
- **Estado:** Aprobada
- **Origen:** Feedback directo del owner

## D-008: Proyecto como contexto global, no nivel de navegación

- **Fecha:** 2026-02-21
- **Contexto:** El plan original proponía 4 niveles: Projects → Test Cases → Runs → Run Detail. Experiencia determinó que 4 niveles es demasiado para MVP.
- **Decisión:** El proyecto se selecciona en la barra superior (dropdown). No hay vista "lista de proyectos". Las vistas son: Tests (home) → Test Detail → Run Detail. 3 niveles, no 4.
- **Reversible:** Sí
- **Estado:** Aprobada
- **Origen:** Experience Architect — SYSTEM.md, JOURNEYS.md

## D-009: Veredicto como elemento de primera clase en el modelo de datos

- **Fecha:** 2026-02-21
- **Contexto:** El modelo original del Run tenía `task_result_json` como campo genérico que contenía todo el resultado. La experiencia requiere que el veredicto (razón de pass/fail) sea lo primero que el usuario ve.
- **Decisión:** Separar `verdict_reason` como campo propio en la tabla `runs`. Renombrar `task_result_json` a `findings_json`. Agregar `steps_json` para la timeline de pasos.
- **Reversible:** Sí
- **Estado:** Aprobada
- **Origen:** Experience Architect — DOMAIN-ADJUSTMENTS.md

## D-010: Onboarding por estados vacíos, no por wizard

- **Fecha:** 2026-02-21
- **Contexto:** El usuario nuevo necesita configurar su primera app. Opciones: wizard de onboarding, o estados vacíos que guíen la acción.
- **Decisión:** Cada estado vacío (sin proyectos, sin tests, sin runs) es una invitación a la siguiente acción. No hay tutorial ni wizard de pasos. El producto guía por contexto.
- **Reversible:** Sí
- **Estado:** Aprobada
- **Origen:** Experience Architect — JOURNEYS.md

## D-011: Style Guide vivo como primer entregable visual

- **Fecha:** 2026-02-21
- **Contexto:** El owner necesita validar el sistema de experiencia visualmente antes de implementar la app. Los documentos markdown no son suficientes. Necesita ver paleta, tokens, componentes en sus estados, journeys, copy — todo renderizado.
- **Decisión:** Construir una ruta `/design` en el frontend que renderice los componentes reales del sistema de experiencia como style guide interactivo. Los componentes se crean como archivos `.vue` en `frontend/src/components/` y la ruta los muestra en modo showcase con documentación inline.
- **Beneficios:** (1) El owner valida antes de integrar, (2) fuerza construcción de componentes aislados, (3) referencia viva de consistencia, (4) progreso observable.
- **Reversible:** Sí (la ruta se puede ocultar en producción)
- **Estado:** Aprobada
- **Origen:** Feedback directo del owner + review de Execution Architect
- **Implementada:** Sí. Decisiones de construcción documentadas en `docs/experience/STYLEGUIDE-DECISIONS.md` (SD-001 a SD-010)
