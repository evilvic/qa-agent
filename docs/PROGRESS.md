# Progress Log

Registro cronológico de avances, bloqueos y cambios de dirección.

---

## 2026-02-21 — Sesión 1: Análisis y planificación

### Lo que se hizo
- Análisis completo del codebase actual (backend, frontend, configuración)
- Definición de contexto del producto (CONTEXT.md)
- Definición de fases de ejecución (PLAN.md)
- Detalle de Fase 1 (phases/PHASE-1.md)
- Detalle de Fase 2 (phases/PHASE-2.md)
- Registro de decisiones iniciales (DECISIONS.md)
- Actualización de CLAUDE.md para reflejar nueva dirección

### Decisiones tomadas
- D-001 a D-006 registradas (ver DECISIONS.md)

### Estado actual
- **Fase activa:** Pre-Fase 1 (planificación + diseño de experiencia)
- **Siguiente acción:** Integrar ajustes de experiencia en PHASE-1.md y empezar implementación

### Bloqueos
- Ninguno identificado

---

## 2026-02-21 — Sesión 1 (continuación): Experience Architect

### Lo que se hizo
- Corrección de dirección: experiencia primero, infraestructura después (D-007)
- Invocación de Experience Architect para definir el sistema de experiencia del MVP
- Creación de `docs/experience/`:
  - `SYSTEM.md` — principios de experiencia, modelo de navegación, semántica visual
  - `JOURNEYS.md` — 6 journeys del usuario detallados con flujos y momentos críticos
  - `COMPONENTS.md` — mapa completo de componentes con estados
  - `DOMAIN-ADJUSTMENTS.md` — cambios al modelo de datos requeridos por la experiencia
- Registro de decisiones D-007 a D-010

### Decisiones tomadas
- D-007: Experiencia guía infraestructura
- D-008: Proyecto como contexto, no navegación (3 niveles, no 4)
- D-009: Veredicto como campo de primera clase en runs
- D-010: Onboarding por estados vacíos

### Cambios al modelo de dominio (de experiencia)
- Run: nuevo campo `verdict_reason`, `steps_json`, renombrar `task_result_json` → `findings_json`
- Project: nuevo campo `is_active`
- API: nuevos endpoints `POST /projects/{id}/activate`, `GET /runs/active`
- Navegación: tests como home, proyecto como selector en top bar

### Estado actual
- **Fase activa:** Pre-Fase 1 — ajustes de experiencia pendientes de integrar en PHASE-1.md
- **Siguiente acción:** Que el owner revise el sistema de experiencia y apruebe antes de implementar

### Bloqueos
- Ninguno

---

## 2026-02-21 — Sesión 1 (cont.): Review + feedback del owner

### Feedback del owner
- Los documentos de experiencia están bien conceptualmente pero necesita verlos VISUALMENTE
- Requiere un style guide dentro del frontend que muestre: paleta, tokens, componentes en sus estados, journeys, copy con ejemplos
- El proceso debe ser observable y documentado
- Execution Architect debe revisar el trabajo de Experience Architect, dar feedback, y autorizar

### Review del Execution Architect
- Sistema de navegación: aprobado (3 niveles, proyecto como contexto)
- Journeys: aprobados (6 journeys cubren el MVP)
- Componentes: aprobados con gaps identificados
- Domain adjustments: aprobados
- Gaps encontrados: (1) paleta incompleta, (2) copy no especificado, (3) loading underspecified, (4) sin breakpoints

### Decisiones
- D-011: Style guide vivo como primer entregable visual (ruta `/design` en frontend)

### Instrucción emitida
- Experience Architect autorizado para escribir código
- Tarea: construir `/design` con componentes reales, paleta, tipografía, estados, journeys, copy
- Los gaps se resuelven durante la construcción
- Review documentado en `docs/experience/REVIEW-EA.md`

### Estado actual
- **Fase activa:** Pre-Fase 1 — style guide construido, pendiente revisión del owner
- **Siguiente acción:** Owner revisa `/design` y aprueba antes de iniciar implementación

---

## 2026-02-21 — Sesión 1 (cont.): Experience Architect construye style guide

### Lo que se hizo
- Experience Architect construyó el style guide completo como ruta `/design` del frontend
- 10 componentes Vue reales creados en `frontend/src/components/`
- Tokens CSS con paleta completa (colores, tipografía, espaciado, sombras, animaciones)
- Vue Router configurado (ruta `/` = app PoC, ruta `/design` = style guide)
- 6 secciones: Colores, Tipografía, Espaciado, Componentes, Journeys, Copy
- Gaps resueltos: paleta completa (SD-001), voz/tuteo (SD-002), glosario español (SD-003), loading pattern (SD-004), breakpoint (SD-005)
- Decisiones documentadas en `docs/experience/STYLEGUIDE-DECISIONS.md` (SD-001 a SD-010)
- Build exitoso, sin errores de compilación

### Componentes construidos
StatusBadge, VerdictCard, RunButton, EmptyState, RunningIndicator, TechnicalDetails, TestRow, TestForm, ProjectSelector

### Estado actual
- **Style guide listo para revisión** — `cd frontend && bun run dev` → `http://localhost:5173/design`
- **Siguiente paso:** Owner revisa, aprueba, y entonces integramos los ajustes de experiencia en PHASE-1.md para empezar a implementar
