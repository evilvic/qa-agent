# Decisiones del Style Guide

Decisiones tomadas durante la construcción del style guide (`/design`).

---

## SD-001: Paleta completa con 4 variantes por estado

Cada color de estado tiene: sólido, fondo (bg), borde, y texto.
- **Sólido:** para íconos, dots, acentos
- **Fondo:** para cards y badges (muy claro, no agresivo)
- **Borde:** para delimitar badges y cards de estado
- **Texto:** para labels y texto sobre fondo claro (alto contraste)

Los colores base vienen de la escala de Tailwind (green-500, red-500, amber-500, blue-500, gray-500) porque tienen buena relación de contraste y son reconocibles universalmente.

## SD-002: Tuteo como voz del producto

El producto habla de "tú". Razones:
- Target user: técnico, no corporativo
- El producto es una herramienta de trabajo, no un sistema institucional
- "Tú" genera cercanía y reduce la distancia entre herramienta y usuario
- Consistente con productos modernos en español (Notion en español, Figma, etc.)

## SD-003: Términos técnicos que se mantienen en inglés

Login, dashboard, timeout: se mantienen porque:
- No tienen equivalente natural en español técnico
- El usuario los reconoce más rápido que sus traducciones
- Traducirlos genera confusión ("inicio de sesión" es más largo y menos preciso)

El resto se traduce: prueba (no test), ejecutar (no run), pasó/falló (no pass/fail en la UI).

## SD-004: Spinners para acciones, no skeletons

Para el MVP, se usan spinners CSS-only para acciones en progreso (ejecutar, guardar).
No se implementan skeleton loaders todavía porque:
- La data local (SQLite) carga instantáneamente
- Solo el run del agente es lento (y ya tiene RunningIndicator)
- Skeletons agregan complejidad visual sin beneficio claro en MVP

Se pueden agregar después si la latencia aumenta (ej: cuando haya API remota).

## SD-005: Un solo breakpoint (768px)

Desktop: >= 769px (layout normal).
Tablet/mobile: <= 768px (stacks, columnas simples).

No se diseña para mobile en el MVP. El uso principal es desktop.
Pero la UI no se rompe en pantallas pequeñas — los grids colapsan a una columna.

## SD-006: Max width 960px

El contenido máximo es 960px en vez de los 1200px del PoC.
Los tests y sus resultados no necesitan tanto ancho. 960px mantiene una línea de lectura cómoda (~75 caracteres) y se siente más enfocado.

## SD-007: RootApp.vue como shell del router

Se creó `RootApp.vue` como shell mínimo que renderiza `<router-view />`.
`App.vue` (el PoC original) se mantiene intacto como la ruta `/` (home temporal).
Esto permite que el style guide funcione sin modificar el código existente.

## SD-008: Componentes con props tipados y validators

Cada componente tiene:
- Props con tipos definidos y validators donde aplica
- Emits declarados explícitamente
- Roles ARIA donde el componente tiene semántica (status, alert, listbox)
- CSS scoped que consume tokens globales

No se usan slots todavía — los componentes son simples y directos.
Se pueden agregar cuando la composición lo requiera.

## SD-009: CSS tokens como custom properties, no preprocesador

Se usan CSS custom properties (`var(--token)`) en vez de SCSS/Less porque:
- Zero config (no necesita build step adicional)
- Runtime theming posible (si algún día se quiere dark mode)
- Compatible con el setup actual de Vite
- Los componentes importan tokens implícitamente (están en `:root`)

## SD-010: Animación con prefers-reduced-motion

El `tokens.css` incluye un media query que desactiva animaciones si el usuario tiene `prefers-reduced-motion: reduce`. Accesibilidad integrada desde el inicio.

---

## Archivos creados

| Archivo | Propósito |
|---------|-----------|
| `src/assets/tokens.css` | Tokens de diseño (colores, tipografía, espaciado, sombras, animaciones) |
| `src/components/StatusBadge.vue` | Badge de estado (pass/fail/error/running/none) |
| `src/components/VerdictCard.vue` | Card de veredicto (el momento de verdad) |
| `src/components/RunButton.vue` | Botón de ejecución (idle/running/disabled, compact) |
| `src/components/EmptyState.vue` | Estado vacío con invitación a acción |
| `src/components/RunningIndicator.vue` | Barra de progreso fija durante ejecución |
| `src/components/TechnicalDetails.vue` | Detalles técnicos colapsables |
| `src/components/TestRow.vue` | Fila de test en lista |
| `src/components/TestForm.vue` | Formulario de crear/editar test |
| `src/components/ProjectSelector.vue` | Dropdown de selección de proyecto |
| `src/views/DesignGuide.vue` | Vista del style guide (`/design`) |
| `src/router/index.js` | Configuración de Vue Router |
| `src/RootApp.vue` | Shell del router |
| `src/main.js` | Entry point actualizado con router y tokens |
