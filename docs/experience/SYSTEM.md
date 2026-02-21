# Sistema de experiencia

## Intención del producto

El usuario tiene una web app. Quiere saber si funciona. No quiere escribir código, no quiere dictar pasos, no quiere aprender Cypress. Quiere decir qué probar, ver si pasó o falló, y confiar en el resultado.

La experiencia debe sentirse como **delegar QA a alguien competente**: le dices qué verificar, te reporta con evidencia.

## Supuestos explícitos

1. El usuario es técnico (sabe qué es un login flow, un selector, una URL) pero no quiere operar herramientas complejas.
2. El uso es desktop-first. QA no se hace desde el celular.
3. El usuario trabaja con 1-3 apps simultáneamente, no 50.
4. Un run tarda 10-120 segundos. Ese tiempo de espera es una experiencia real que hay que diseñar.
5. El MVP es single-user. No hay colaboración, no hay roles, no hay permisos.

## Principios de experiencia

### 1. El veredicto es lo primero
Cuando un test termina, lo primero que ves es: **pasó o falló**. Grande, claro, sin ambigüedad. Todo lo demás (screenshots, datos, timing) es evidencia de soporte. El veredicto nunca se pierde en un dump de datos.

### 2. Los tests son el centro
El objeto principal del producto es el test case. No el proyecto, no el run, no la configuración. El usuario piensa "mis tests". Los proyectos son contexto, los runs son historial. Los tests son lo que importa.

### 3. Cada estado vacío es una invitación
"No tienes proyectos" no es un error, es una oportunidad: "Configura tu primera app para empezar." Cada pantalla vacía guía al siguiente paso.

### 4. La espera es parte de la experiencia
Un run de 30-90 segundos es un momento de ansiedad. La UI debe comunicar que algo está pasando, qué está pasando, y que eventualmente terminará. No solo un spinner.

### 5. Lo técnico se esconde hasta que se necesita
Modelo usado, tokens consumidos, selectores, execution path: información valiosa que no necesitas ver siempre. Disponible cuando la buscas, invisible cuando no.

### 6. Español nativo, no traducido
La UI habla español como idioma primario. No es una traducción de una app en inglés. El copy es natural, directo, sin anglicismos innecesarios.

## Modelo de navegación

```
┌─────────────────────────────────────────────┐
│ [Logo/Nombre]    [Proyecto activo ▾]        │  ← Barra superior fija
├─────────────────────────────────────────────┤
│                                             │
│  Vista principal (cambia según contexto):   │
│                                             │
│  1. Lista de tests     (home)               │
│  2. Detalle de test    (test + sus runs)    │
│  3. Detalle de run     (evidencia completa) │
│  4. Configuración      (proyecto activo)    │
│                                             │
└─────────────────────────────────────────────┘
```

### Por qué esta estructura

- **3 niveles funcionales, no 4.** El plan original proponía Projects → Test Cases → Runs → Run Detail. Cuatro niveles es demasiado profundo para MVP. En su lugar: el proyecto se selecciona arriba (como contexto), y las vistas son Tests → Test+Runs → Run Detail.
- **El proyecto es contexto, no navegación.** Cambiar de proyecto es como cambiar de workspace, no navegar a otra pantalla. Un dropdown en la barra superior basta.
- **La home son los tests.** Al abrir la app, ves tus tests y su estado. No una pantalla de bienvenida, no un dashboard de métricas, no una lista de proyectos.

## Flujo de primera vez (onboarding)

```
App sin proyectos
  → Estado vacío: "Configura tu primera app"
  → Formulario inline o modal: nombre, URL, credenciales
  → Proyecto creado, se activa automáticamente

Proyecto sin tests
  → Estado vacío: "Crea tu primera prueba"
  → Formulario: nombre, instrucciones, resultado esperado
  → Test creado, botón "Ejecutar" visible

Primer run
  → Click "Ejecutar"
  → Estado running con progreso
  → Resultado: PASS/FAIL con evidencia
  → El usuario entiende el ciclo completo
```

No hay tutorial, no hay wizard de 5 pasos. El estado vacío ES el onboarding.

## Semántica de color

| Estado | Color | Uso |
|--------|-------|-----|
| Pass | Verde (`#22c55e`) | Veredicto positivo, badge, borde |
| Fail | Rojo (`#ef4444`) | Veredicto negativo, badge, borde |
| Error | Ámbar (`#f59e0b`) | Error de sistema (no del test), badge, borde |
| Running | Azul (`#3b82f6`) | En ejecución, spinner, pulso |
| Neutro | Gris (`#6b7280`) | Sin ejecutar, información secundaria |

Estos colores tienen significado consistente en TODO el producto. Un badge verde siempre significa "pasó". No hay reinterpretación por contexto.

## Tipografía y espaciado

- **Font:** System stack (ya definido en el PoC, correcto para MVP)
- **Escala:** 14px base, 16px para lectura principal, 12px para metadata
- **Espaciado:** Múltiplos de 4px (4, 8, 12, 16, 24, 32, 48)
- **Max width contenido:** 960px (no 1200 — los tests no necesitan tanto ancho)
- **Densidad:** Media. No tan compacto como una IDE, no tan espaciado como un landing page.
