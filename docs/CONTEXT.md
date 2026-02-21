# Contexto del producto

## Origen

Este proyecto nace de la experiencia con un producto de QA automation que se contrató externamente (~$500 USD/mes). Ese producto funciona, pero tiene limitaciones claras. La decisión fue replicar y superar sus capacidades con un sistema propio.

## Producto de referencia (competidor)

**Cómo funciona:**
- Plataforma web donde el usuario escribe test cases paso a paso
- Cada paso es una instrucción: "revisa que cargue la página", "pon este usuario aquí", "haz click en iniciar sesión"
- Los tests corren y dan resultado pass/fail con screenshots
- Instrucción por instrucción, manual, tedioso

**Limitaciones identificadas:**
- No maneja pruebas negativas (contraseña incorrecta, campos vacíos, errores esperados)
- Cada run empieza desde cero, sin memoria de ejecuciones anteriores
- Requiere escribir cada paso manualmente, sin autonomía del agente
- No propone qué probar, solo ejecuta lo que le dictan

## Visión del producto

Un sistema de QA autónomo con tres niveles de inteligencia creciente:

### Nivel 1 — Ejecución con intención (no paso a paso)
El usuario describe QUE quiere probar en lenguaje natural, no COMO hacerlo. El agente descubre el camino.

### Nivel 2 — Memoria entre ejecuciones
El agente recuerda qué funcionó (selectores, rutas, secuencias) y reutiliza ese conocimiento. Solo redescubre cuando algo cambió. Esto reduce costo y tiempo.

### Nivel 3 — Autonomía y descubrimiento
El agente explora la app, mapea flujos, propone test cases, genera variantes negativas. El usuario valida y ajusta, no dicta.

## Principios de producto

1. **App-agnostic** — Funciona con cualquier web app, no está atado a una app específica
2. **Español como idioma nativo** — Instrucciones, prompts, UI en español (expandible a otros idiomas después)
3. **Intención > instrucción** — El usuario dice qué quiere, no cómo hacerlo
4. **Memoria > repetición** — Cada ejecución deja conocimiento reutilizable
5. **Costo consciente** — Usar el modelo más barato que pueda resolver la tarea
6. **Pass/fail claro** — Cada test tiene un veredicto explícito con evidencia

## Target user (MVP)

- Por ahora: el propio creador del producto, probando contra proyectos propios
- Después: equipos de QA/producto de empresas pequeñas-medianas
- No se necesita auth ni multi-tenant en el MVP

## Restricciones

- Presupuesto de OpenAI es un constraint real → optimizar costo por run
- El agente usa `browser_use` + Playwright → dependencia fuerte en esta librería
- MVP corre local (no hay deploy todavía)
