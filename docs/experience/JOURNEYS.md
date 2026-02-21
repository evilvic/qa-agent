# Journeys del usuario

## Journey 1: Configurar mi primera app

### Trigger
El usuario acaba de instalar/abrir la app por primera vez. No hay proyectos.

### Flujo

```
[Pantalla vacía]
  "No hay proyectos configurados"
  "Para empezar, configura la app que quieres probar."
  [Botón: Configurar app]

    ↓

[Formulario de proyecto — modal o panel lateral]
  - Nombre del proyecto (ej: "Mi tienda online")
  - URL base (ej: "https://miapp.com")
  - Ruta de login (ej: "/login", opcional)
  - Email de acceso
  - Contraseña de acceso
  - Descripción breve (opcional, para contexto del agente)
  [Guardar]

    ↓

[Proyecto creado → se activa automáticamente]
[Redirige a lista de tests → estado vacío del proyecto]
```

### Momento crítico
El usuario necesita entender QUE datos poner y POR QUE. Los campos deben tener placeholders descriptivos y helper text cuando sea necesario. La contraseña es sensible — indicar que se almacena localmente.

### Estados de error
- URL inválida → validación inline, no bloquear submit
- Campos requeridos vacíos → indicar cuáles faltan

---

## Journey 2: Crear un test

### Trigger
El usuario tiene un proyecto activo pero quiere probar algo específico.

### Flujo

```
[Lista de tests — con o sin tests existentes]
  [Botón: + Nuevo test]

    ↓

[Formulario de test — inline o expandible, NO nueva página]
  - Nombre (corto, para la lista)
    placeholder: "Login con credenciales válidas"
  - Instrucciones (qué debe hacer el agente)
    placeholder: "Inicia sesión con las credenciales del proyecto.
                  Navega al dashboard principal."
    helper: "Describe la intención, no los pasos exactos.
             El agente descubrirá cómo hacerlo."
  - Resultado esperado (cómo saber si pasó)
    placeholder: "Se muestra el dashboard con el nombre del usuario visible."
    helper: "¿Qué debería verse en la pantalla si todo salió bien?"
  [Guardar]

    ↓

[Test creado → aparece en la lista]
[Botón "Ejecutar" visible junto al test]
```

### Decisiones de experiencia

**¿Por qué inline y no una página nueva?** Crear un test es una acción rápida. No debería sentirse como llenar un formulario largo. El usuario está en contexto (mirando sus tests), la creación debería ser parte de ese flujo, no una interrupción.

**¿Por qué tres campos separados (nombre, instrucciones, resultado esperado)?** Porque cada uno tiene un propósito distinto:
- El **nombre** es para la lista (identificar rápido)
- Las **instrucciones** son para el agente (qué hacer)
- El **resultado esperado** es para el veredicto (cómo evaluar)

Combinarlos en un solo campo haría la evaluación pass/fail más ambigua.

---

## Journey 3: Ejecutar un test

### Trigger
El usuario quiere correr un test (nuevo o existente).

### Flujo

```
[Lista de tests]
  Click [Ejecutar] en un test

    ↓

[El test pasa a estado "running"]
  - Badge azul "Ejecutando..." con animación
  - En la fila del test, se muestra indicador de progreso
  - El botón Ejecutar se deshabilita
  - Opcionalmente: contador de tiempo transcurrido

    ↓ (10-120 segundos)

[Run completo → resultado aparece]
  - Badge cambia a PASS (verde) / FAIL (rojo) / ERROR (ámbar)
  - La fila del test se actualiza con el último resultado
  - Notificación sutil (no intrusiva) de que terminó
  - Click en el resultado → va al detalle del run
```

### Momento crítico: la espera

Este es el momento más frágil de la experiencia. 30-90 segundos sin feedback genera ansiedad. Opciones:

**Mínimo viable (Fase 1):**
- Badge "Ejecutando..." con animación de pulso
- Contador de segundos transcurridos
- Texto: "El agente está navegando tu app..."

**Mejor (futuro):**
- Live feed de lo que el agente está haciendo
- Screenshots en tiempo real
- Pasos completados en una timeline

Para el MVP, el mínimo viable es suficiente. La clave es que el usuario SEPA que algo está pasando y que no se colgó.

### Ejecución desde detalle del test
El usuario también puede ejecutar un test desde la vista de detalle (no solo desde la lista). El comportamiento es el mismo pero el resultado se muestra inline en la vista de detalle.

---

## Journey 4: Ver el resultado de un run

### Trigger
Un run terminó, o el usuario revisa un run histórico.

### Flujo

```
[Click en un run (desde lista o desde notificación)]

    ↓

[Vista de detalle del run]

  ┌──────────────────────────────────────────┐
  │ ● PASÓ                                   │  ← Veredicto: grande, color, claro
  │ "El login fue exitoso. Se llegó al       │
  │  dashboard y el nombre del usuario es     │
  │  visible en la barra superior."           │  ← Razón: una o dos oraciones
  ├──────────────────────────────────────────┤
  │ Evidencia                                │
  │ ┌────┐ ┌────┐ ┌────┐ ┌────┐            │
  │ │ S1 │ │ S2 │ │ S3 │ │ S4 │            │  ← Timeline de screenshots
  │ └────┘ └────┘ └────┘ └────┘            │
  │ Paso 1: Navegó a /login                  │
  │ Paso 2: Ingresó credenciales             │
  │ Paso 3: Hizo click en "Entrar"           │
  │ Paso 4: Dashboard cargado               │  ← Pasos con descripción
  ├──────────────────────────────────────────┤
  │ ▸ Detalles técnicos                      │  ← Colapsado por default
  │   Modelo: gpt-4.1-mini                   │
  │   Tokens: 2,340                           │
  │   Duración: 34.2s                        │
  │   URL final: https://app.com/dashboard   │
  └──────────────────────────────────────────┘
```

### Jerarquía de información (no negociable)

1. **Veredicto** — PASÓ / FALLÓ / ERROR. Lo primero que ves. Sin desplazarte.
2. **Razón** — Por qué pasó o falló. En lenguaje humano, no JSON.
3. **Evidencia visual** — Screenshots en orden cronológico. Cada uno con su paso.
4. **Detalles técnicos** — Colapsados. Modelo, tokens, tiempo, URLs.

El PoC actual invierte esta jerarquía: muestra IDs y metadata arriba, resultado abajo. Eso está al revés.

---

## Journey 5: Revisar historial de un test

### Trigger
El usuario quiere ver cómo ha evolucionado un test a lo largo del tiempo.

### Flujo

```
[Click en un test case (desde la lista)]

    ↓

[Vista de detalle del test case]

  ┌──────────────────────────────────────────┐
  │ Login con credenciales válidas       [✎] │  ← Nombre (editable)
  │                                          │
  │ Instrucciones:                           │
  │ "Inicia sesión con las credenciales..."  │
  │                                          │
  │ Resultado esperado:                      │
  │ "Dashboard visible con nombre de..."     │
  │                                          │
  │ [Ejecutar ahora]                         │
  ├──────────────────────────────────────────┤
  │ Historial de ejecuciones                 │
  │                                          │
  │ ● Hoy 14:32    PASÓ     34.2s           │
  │ ● Hoy 10:15    FALLÓ    28.7s           │
  │ ● Ayer 16:45   PASÓ     41.1s           │
  │ ● 19 feb       ERROR    120.0s (timeout)│
  │                                          │
  │ Click en cualquier run → detalle         │
  └──────────────────────────────────────────┘
```

### Lo que comunica esta vista
- El test case es **el objeto persistente** — lo que defines una vez y ejecutas muchas.
- El historial muestra **tendencia** — ¿este test pasa consistentemente o es flaky?
- Los errores de sistema (timeouts) son visualmente distintos de los fallos del test.

---

## Journey 6: Cambiar de proyecto

### Trigger
El usuario quiere probar una app diferente.

### Flujo

```
[Click en selector de proyecto (barra superior)]

    ↓

[Dropdown con proyectos existentes]
  ✓ Mi tienda online
    API de pagos
    App móvil staging
  ──────────
  + Nuevo proyecto

    ↓

[Click en otro proyecto]
  → La lista de tests cambia al proyecto seleccionado
  → Todo el contexto cambia (tests, runs, configuración)
```

Simple. No hay página de "mis proyectos". El selector IS la interfaz de proyectos para el MVP.
