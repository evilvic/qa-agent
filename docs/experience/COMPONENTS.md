# Componentes y estados

## Mapa de componentes

```
App
├── TopBar
│   ├── Logo / Nombre del producto
│   └── ProjectSelector (dropdown)
│
├── Router View
│   ├── TestList (home)
│   │   ├── TestListHeader (título + botón nuevo)
│   │   ├── TestListEmpty (estado vacío)
│   │   ├── TestRow (por cada test) ×N
│   │   │   ├── StatusBadge
│   │   │   └── RunButton
│   │   └── TestForm (crear/editar — expandible inline)
│   │
│   ├── TestDetail (detalle de un test + historial)
│   │   ├── TestInfo (nombre, instrucciones, expected outcome)
│   │   ├── RunButton
│   │   ├── RunTimeline (historial de runs)
│   │   │   └── RunRow ×N
│   │   │       └── StatusBadge
│   │   └── TestForm (modo edición)
│   │
│   ├── RunDetail (detalle de un run)
│   │   ├── VerdictCard (PASS/FAIL/ERROR + razón)
│   │   ├── StepsTimeline (screenshots + pasos)
│   │   │   └── StepCard ×N
│   │   └── TechnicalDetails (colapsable)
│   │
│   └── ProjectSettings (configuración del proyecto activo)
│       └── ProjectForm
│
├── ProjectSetup (modal — primera vez, sin proyectos)
│   └── ProjectForm
│
└── RunningIndicator (overlay/toast cuando hay un run activo)
```

---

## Componentes detallados

### TopBar

**Propósito:** Contexto global. ¿En qué app estoy? Navegación mínima.

**Contenido:**
- Izquierda: nombre del producto (link a home)
- Derecha: ProjectSelector + link a configuración

**Estado único.** No cambia. Siempre visible.

---

### ProjectSelector

**Propósito:** Cambiar de proyecto (app target) sin navegar a otra página.

| Estado | Comportamiento |
|--------|---------------|
| Sin proyectos | No se muestra. El modal ProjectSetup toma control. |
| Un proyecto | Muestra nombre del proyecto. Click abre dropdown con opción "+ Nuevo proyecto". |
| Varios proyectos | Dropdown con lista. Check mark en el activo. Opción "+ Nuevo proyecto" al final. |

---

### TestList (vista principal / home)

**Propósito:** Ver todos los tests del proyecto activo. Ejecutar. Crear nuevos.

| Estado | Lo que se muestra |
|--------|-------------------|
| **Vacío** (sin tests) | `TestListEmpty`: "No hay pruebas todavía. Crea tu primera prueba para empezar." + botón "Crear prueba". |
| **Con tests** | Lista de `TestRow`. Header con título "Pruebas" y botón "+ Nueva prueba". |
| **Con run activo** | El `TestRow` del test en ejecución muestra estado "running" con animación. Los demás tests siguen disponibles. |

---

### TestRow

**Propósito:** Una fila en la lista de tests. Resumen visual rápido.

**Contenido:**
```
┌─────────────────────────────────────────────────────┐
│ ● [badge]  Nombre del test                    [▶]  │
│            Última ejecución: hace 2 horas           │
└─────────────────────────────────────────────────────┘
```

- **StatusBadge**: color según último run (pass/fail/error/sin ejecutar)
- **Nombre**: click → va a TestDetail
- **Metadata**: última ejecución (tiempo relativo)
- **RunButton**: botón compacto para ejecutar directamente

| Estado del último run | Badge | Color |
|----------------------|-------|-------|
| Nunca ejecutado | — | Gris |
| Pass | Pasó | Verde |
| Fail | Falló | Rojo |
| Error | Error | Ámbar |
| Running | Ejecutando... | Azul + animación |

---

### StatusBadge

**Propósito:** Indicador visual del estado de un run. Reutilizable en toda la app.

**Variantes:**
- `pass` → texto "Pasó", fondo verde claro, borde verde, texto verde oscuro
- `fail` → texto "Falló", fondo rojo claro, borde rojo, texto rojo oscuro
- `error` → texto "Error", fondo ámbar claro, borde ámbar, texto ámbar oscuro
- `running` → texto "Ejecutando...", fondo azul claro, borde azul, texto azul oscuro, animación pulso
- `none` → texto "Sin ejecutar", fondo gris claro, borde gris, texto gris

---

### RunButton

**Propósito:** Disparar un run de un test case.

| Estado | Apariencia | Acción |
|--------|-----------|--------|
| Idle | Botón azul "Ejecutar" o ícono ▶ | Click → inicia run |
| Running | Botón deshabilitado, muestra spinner | No clickeable |
| Disabled | Gris, opaco | Cuando no hay proyecto activo o datos incompletos |

---

### TestForm

**Propósito:** Crear o editar un test case. Inline (no nueva página).

**Campos:**
1. **Nombre** — input text. Required. Max ~100 chars.
   - placeholder: "Login exitoso"
2. **Instrucciones** — textarea. Required.
   - placeholder: "Inicia sesión con las credenciales del proyecto y navega al dashboard."
   - helper text: "Describe qué quieres probar. El agente descubrirá cómo hacerlo."
3. **Resultado esperado** — textarea. Required.
   - placeholder: "El dashboard se muestra con el nombre del usuario visible."
   - helper text: "¿Cómo sabes si la prueba pasó? ¿Qué debería verse en pantalla?"

**Acciones:** Guardar / Cancelar

| Estado | Comportamiento |
|--------|---------------|
| Crear | Campos vacíos. Aparece debajo del header o como primera fila expandida. |
| Editar | Campos pre-poblados. Aparece inline reemplazando el display del test. |
| Validación | Campos requeridos marcados si están vacíos al intentar guardar. |
| Guardando | Botón deshabilitado con indicador. |

---

### TestDetail

**Propósito:** Ver un test case completo con su historial de runs.

**Estructura:**
```
[← Volver a pruebas]

┌─────────────────────────────────────────┐
│ Login con credenciales válidas     [✎]  │
│                                         │
│ Instrucciones:                          │
│ "Inicia sesión con..."                  │
│                                         │
│ Resultado esperado:                     │
│ "El dashboard se muestra..."            │
│                                         │
│ [Ejecutar ahora]                        │
├─────────────────────────────────────────┤
│ Historial                               │
│                                         │
│ (lista de RunRow)                       │
└─────────────────────────────────────────┘
```

| Estado | Comportamiento |
|--------|---------------|
| Sin runs | Sección historial: "Esta prueba no se ha ejecutado. Haz click en Ejecutar para correrla." |
| Con runs | Lista cronológica (más reciente arriba). |
| Run activo | RunRow activo con animación + botón Ejecutar deshabilitado. |
| Modo edición | Los campos se vuelven editables (TestForm inline). |

---

### RunDetail

**Propósito:** Evidencia completa de una ejecución. LA vista más importante del producto.

**Estructura (ver JOURNEYS.md Journey 4):**

```
[← Volver al test]

┌─ VerdictCard ──────────────────────────┐
│ ● PASÓ                                 │
│ "El login fue exitoso..."              │
└────────────────────────────────────────┘

┌─ StepsTimeline ────────────────────────┐
│ Paso 1 → Paso 2 → Paso 3 → Paso 4    │
│ [screenshot] [screenshot] ...          │
│ Navegó     Escribió    Clickeó   Listo│
└────────────────────────────────────────┘

▸ Detalles técnicos (colapsado)
```

| Estado | Comportamiento |
|--------|---------------|
| Pass | VerdictCard verde. StepsTimeline muestra el camino exitoso. |
| Fail | VerdictCard roja. Razón explica qué se esperaba vs qué se encontró. |
| Error | VerdictCard ámbar. Mensaje de error (timeout, crash, etc). StepsTimeline muestra hasta dónde llegó. |
| Sin screenshots | StepsTimeline no se muestra. Solo veredicto + detalles técnicos. |

---

### VerdictCard

**Propósito:** El momento de verdad. ¿Pasó o falló?

**Estructura:**
```
┌────────────────────────────────────────┐
│ ● PASÓ                                 │  ← Status + color dominante
│                                        │
│ El login fue exitoso. Se llegó al      │
│ dashboard y el nombre del usuario      │
│ es visible en la barra superior.       │  ← Razón del veredicto
└────────────────────────────────────────┘
```

- Fondo: color del estado (verde claro / rojo claro / ámbar claro)
- Borde izquierdo grueso del color del estado
- Texto del veredicto: grande (18-20px), bold
- Texto de la razón: tamaño normal, debajo

---

### StepsTimeline

**Propósito:** Mostrar qué hizo el agente, paso a paso, con evidencia visual.

**Estructura:**
```
┌────────────────────────────────────────┐
│  [img1]     [img2]     [img3]          │  ← Screenshots en fila
│   Paso 1     Paso 2     Paso 3         │
│  Navegó a   Ingresó    Click en        │
│  /login     email      "Entrar"        │  ← Descripción del paso
└────────────────────────────────────────┘
```

- Horizontal scroll si hay más de 3-4 screenshots
- Click en screenshot → ampliar (modal o lightbox)
- Cada paso tiene: número, screenshot thumbnail, descripción breve, URL

---

### TechnicalDetails

**Propósito:** Información técnica para debugging. No es lo principal.

**Contenido:**
- Modelo usado (ej: gpt-4.1-mini)
- Tokens consumidos
- Duración total
- URL final
- Run ID (para referencia)

**Comportamiento:** Colapsado por defecto. Click en header → expande. Persiste en la sesión (si lo abrí, sigue abierto mientras navego entre runs del mismo test).

---

### ProjectForm

**Propósito:** Configurar un proyecto (app target).

**Campos:**
1. **Nombre** — input text. Required.
   - placeholder: "Mi tienda online"
2. **URL base** — input url. Required.
   - placeholder: "https://miapp.com"
   - Validación: URL válida
3. **Ruta de login** — input text. Opcional.
   - placeholder: "/login"
   - helper: "Deja vacío si la app no tiene login"
4. **Email** — input email. Required.
   - placeholder: "usuario@ejemplo.com"
5. **Contraseña** — input password. Required.
   - helper: "Se almacena solo localmente"
6. **Descripción** — textarea. Opcional.
   - placeholder: "Tienda online con catálogo, carrito y checkout."
   - helper: "Ayuda al agente a entender tu app"

**Contextos de uso:**
- Modal `ProjectSetup` (primera vez, sin proyectos)
- Página `ProjectSettings` (editar proyecto existente)

---

### ProjectSetup (modal)

**Propósito:** Onboarding de primera vez.

Se muestra SOLO cuando no hay ningún proyecto. No se puede cerrar sin crear uno (no hay nada que hacer sin proyecto).

Contiene: título descriptivo + ProjectForm + botón crear.

```
┌────────────────────────────────────────────────┐
│                                                │
│   Configura tu primera app                     │
│                                                │
│   Para empezar a crear pruebas, necesitamos    │
│   saber qué app quieres probar.               │
│                                                │
│   (ProjectForm)                                │
│                                                │
│   [Crear proyecto]                             │
│                                                │
└────────────────────────────────────────────────┘
```

---

### RunningIndicator

**Propósito:** Feedback persistente cuando hay un run activo, incluso si el usuario navega a otra vista.

**Comportamiento:**
- Aparece como una barra fija (bottom o top) cuando hay un run en progreso
- Muestra: nombre del test + tiempo transcurrido + animación
- Click → navega al test que está corriendo
- Desaparece cuando el run termina
- Si el usuario ya está viendo el test que corre, no se duplica

```
┌────────────────────────────────────────────────┐
│ ◉ Ejecutando "Login exitoso" — 23s...    [Ver] │
└────────────────────────────────────────────────┘
```
