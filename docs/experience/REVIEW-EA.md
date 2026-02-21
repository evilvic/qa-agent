# Review de Execution Architect sobre el sistema de experiencia

**Fecha:** 2026-02-21
**Revisado por:** Execution Architect
**Documentos revisados:** SYSTEM.md, JOURNEYS.md, COMPONENTS.md, DOMAIN-ADJUSTMENTS.md

---

## Feedback del owner (textual)

> "Necesito algo visual. Veo que se bajaron archivos — existe en journeys, en componentes. Me gustaría que dentro del frontend haya una sección que me muestre: la paleta de colores, los tokens, los componentes en sus distintos estados, los diagramas de los journeys, la parte del look and feel, en qué se basa el tipo de copies propuestos y por qué, con ejemplos."

> "Es importante también tener esta parte de memoria de lo que está haciendo, que también sea observable el trabajo."

**Traducción a requisitos:**
1. Construir una **página de style guide viva** dentro del frontend (`/design`) que renderice el sistema de experiencia como componentes reales, no como markdown.
2. El proceso del Experience Architect debe ser **documentado y observable** — cada decisión visual, cada componente, con su razonamiento.

---

## Review: lo que está bien

### Estructura de navegación (SYSTEM.md)
- **Aprobado.** 3 niveles en vez de 4 es correcto. Proyecto como contexto global simplifica toda la UX.
- La metáfora de "workspace" para el selector de proyecto es clara.

### Journeys (JOURNEYS.md)
- **Aprobado.** Los 6 journeys cubren el ciclo completo del MVP.
- Los "momentos críticos" están bien identificados (la espera del run, el onboarding).
- La decisión de formularios inline para crear tests es correcta — mantiene contexto.

### Componentes (COMPONENTS.md)
- **Aprobado con ajustes.** El árbol de componentes es completo y los estados están bien definidos.
- Ver gaps identificados abajo.

### Domain adjustments (DOMAIN-ADJUSTMENTS.md)
- **Aprobado.** `verdict_reason` como campo propio es la decisión correcta.
- `steps_json` resuelve el problema de las listas paralelas.
- `is_active` en Project es simple y funcional.

---

## Review: gaps identificados

### 1. Paleta de colores incompleta
SYSTEM.md define 5 colores semánticos (pass, fail, error, running, neutro) pero no define:
- Variantes: fondo claro, borde, texto oscuro para cada uno (los specs de componentes las mencionan pero sin valores hex)
- Color de superficie: fondos de cards, fondos de página, bordes generales
- Color de texto: primario, secundario, disabled
- Color de acción: botones primarios, hover, focus

**Acción:** Completar la paleta con todas las variantes que los componentes necesitan.

### 2. Sistema de copy no especificado
SYSTEM.md dice "español nativo, directo, sin anglicismos" pero no define:
- Patrón de voz (¿tutea o habla de usted? ¿formal o casual?)
- Copy para estados de error (mensajes tipo)
- Copy para confirmaciones y acciones destructivas
- Ejemplos de buenos y malos copies

**Acción:** Definir un mini sistema de copy con ejemplos concretos.

### 3. Estados de loading underspecified
Los componentes mencionan estados de loading pero no definen:
- ¿Skeleton placeholders o spinners?
- ¿Cómo se ve la carga inicial de la lista de tests?
- ¿Cómo se ve la transición de "running" a "resultado"?

**Acción:** Definir el patrón de loading (skeleton vs spinner) y aplicarlo a los componentes principales.

### 4. Sin responsive breakpoints detallados
SYSTEM.md dice "desktop-first" pero no define breakpoints ni cómo se adaptan los componentes.

**Acción:** Para MVP, definir un solo breakpoint (desktop vs tablet). Mobile no es prioridad pero no debe romperse.

---

## Decisión: Style Guide como primer entregable

**Contexto:** El owner necesita ver el sistema de experiencia ANTES de que se implemente en la app real. Los markdown no son suficientes para validación visual.

**Decisión:** Construir una ruta `/design` en el frontend que funcione como style guide vivo. Esta ruta:

1. **Renderiza componentes reales** — no mockups ni imágenes. Los mismos componentes que usará la app.
2. **Muestra todos los estados** — cada componente en sus variantes (pass, fail, error, running, vacío).
3. **Documenta las decisiones** — por qué estos colores, por qué este copy, por qué esta jerarquía.
4. **Es el puente entre diseño e implementación** — al construir el style guide, se construyen los componentes. Después solo hay que ensamblarlos en las vistas reales.

**Beneficios:**
- El owner puede revisar y aprobar visualmente
- Fuerza a construir componentes aislados antes de integrarlos
- Sirve como referencia viva para mantener consistencia
- Es observable: se ve el progreso componente por componente

**Registrado como decisión D-011 en DECISIONS.md.**

---

## Instrucción para Experience Architect

### Tarea: Construir el Style Guide (`/design`)

**Secciones del style guide:**

1. **Paleta de colores** — Swatches renderizados con hex, nombre semántico, y uso.
2. **Tipografía** — Escala tipográfica renderizada con ejemplos.
3. **Espaciado** — Escala de spacing visual.
4. **Componentes** — Cada componente en todos sus estados:
   - StatusBadge (pass, fail, error, running, none)
   - VerdictCard (pass, fail, error)
   - RunButton (idle, running, disabled)
   - TestRow (con cada estado de badge)
   - TestForm (vacío, con datos, validación)
   - Empty states (sin proyectos, sin tests, sin runs)
   - RunningIndicator
   - TechnicalDetails (colapsado, expandido)
5. **Journeys** — Diagramas visuales de los 6 flujos (HTML/CSS, no ASCII).
6. **Copy** — Principios de voz con ejemplos de bien/mal, copies para estados vacíos, errores, confirmaciones.

**Restricciones:**
- Usar Vue 3 Composition API
- Construir los componentes como archivos `.vue` reales en `frontend/src/components/`
- La ruta `/design` importa y renderiza estos componentes en modo showcase
- No instalar librerías de UI. CSS propio basado en los tokens definidos.
- Documentar cada decisión visual dentro del propio style guide (texto en la página, no solo en markdown).

**Los gaps identificados (paleta completa, sistema de copy, loading patterns, breakpoints) deben resolverse DURANTE la construcción del style guide, no antes.** Construir es el mejor way de cerrar gaps.
