# Ajustes al modelo de dominio desde experiencia

Este documento registra los cambios que el sistema de experiencia necesita respecto al modelo de dominio propuesto en `docs/PLAN.md` y `docs/phases/PHASE-1.md`.

## Cambios al modelo

### 1. Project: agregar campo `is_active`

**Por qué:** La UI necesita saber cuál es el proyecto activo (el que se muestra en el selector de la barra superior). Solo un proyecto está activo a la vez.

```diff
 projects
 ├── id
 ├── name
 ├── base_url
 ├── login_path
 ├── credentials_email
 ├── credentials_password
 ├── description
 ├── viewport_width
 ├── viewport_height
+├── is_active: bool (default false, solo uno puede ser true)
 ├── created_at
 └── updated_at
```

**Alternativa:** Guardar el proyecto activo en localStorage del frontend. Pero si lo guardamos en el backend, el estado es consistente aunque cambies de browser.

**Decisión:** Backend. Endpoint `POST /projects/{id}/activate`.

---

### 2. Run: separar `verdict_reason` y `verdict_evidence` del JSON genérico

**Por qué:** La razón del veredicto y la evidencia son elementos de primera clase en la UI (VerdictCard). No deben estar enterrados en `task_result_json`.

```diff
 runs
 ├── id
 ├── test_case_id
 ├── status (running | pass | fail | error)
+├── verdict_reason: str | null  — "El login fue exitoso, se llegó al dashboard"
 ├── error_message: str | null   — solo para status=error
 ├── screen_json
-├── task_result_json
+├── findings_json: str | null   — datos extraídos por el agente (flexible)
 ├── execution_path_json
 ├── model_used
 ├── tokens_used
 ├── elapsed_ms
 ├── artifacts_path
 ├── created_at
 └── finished_at
```

**Cambios:**
- `task_result_json` → `findings_json` (nombre más claro)
- Nuevo: `verdict_reason` — la explicación humana del veredicto, primera clase
- Se elimina `verdict_evidence` como campo separado — la evidencia SON los screenshots y los steps. No necesita un campo de texto adicional.

---

### 3. Run: agregar `steps_json` para la timeline

**Por qué:** La StepsTimeline necesita una estructura más rica que solo una lista de paths de screenshots. Cada paso tiene: acción, screenshot, URL, descripción.

```diff
 runs
 ├── ...
+├── steps_json: str | null — JSON array de pasos
 ├── ...
```

**Estructura de `steps_json`:**
```json
[
  {
    "step_number": 1,
    "action": "navigate",
    "description": "Navegó a /login",
    "url": "https://app.com/login",
    "screenshot_path": "artifacts/run_id/screens/step_001.png"
  },
  {
    "step_number": 2,
    "action": "type",
    "description": "Ingresó email en campo de login",
    "url": "https://app.com/login",
    "screenshot_path": "artifacts/run_id/screens/step_002.png"
  }
]
```

Esto reemplaza los campos `screenshots` y `urls` de la response actual (RunResponse), que son dos listas paralelas sin relación explícita.

---

### 4. Navegación: proyecto como contexto, no como nivel de navegación

**Por qué:** El plan original proponía endpoints anidados tipo `/projects/{project_id}/test-cases`. La experiencia dice que el proyecto es **contexto global**, no parte de la navegación. El usuario no "navega a un proyecto" — lo selecciona arriba.

**Implicación en API:**
- Mantener `POST /projects/{project_id}/test-cases` para crear (necesita el FK)
- Pero `GET /test-cases?project_id=X` es más práctico que `GET /projects/{project_id}/test-cases`
- El frontend pasa el `project_id` activo como query param, no como parte de la ruta

**Implicación en frontend:**
- No hay vista "Lista de proyectos" como página
- El selector de proyecto en la TopBar es la única interfaz para proyectos
- La configuración del proyecto es una vista separada (settings), no una lista con drill-down

---

### 5. Endpoint para run activo

**Por qué:** El RunningIndicator necesita saber si hay un run en progreso, incluso si el usuario navega a otra vista.

**Nuevo endpoint:** `GET /runs/active` → retorna el run con status=running (si existe) o 204 si no hay ninguno.

**Alternativa:** El frontend puede trackear esto localmente (sabe cuándo disparó un run). Pero si recarga la página, pierde el estado.

**Decisión:** Ambos. El frontend trackea localmente + verifica con el backend al cargar.

---

## Cambios a la API propuesta

### Endpoints que se mantienen igual
- `POST /projects` — crear proyecto
- `GET /projects` — listar proyectos
- `GET /projects/{id}` — detalle
- `PUT /projects/{id}` — editar
- `DELETE /projects/{id}` — borrar
- `POST /test-cases/{id}/run` — ejecutar
- `GET /runs/{id}` — detalle de run
- `GET /healthz` — health check

### Endpoints nuevos
- `POST /projects/{id}/activate` — marcar como activo
- `GET /runs/active` — run en progreso (si existe)

### Endpoints modificados
- `GET /test-cases?project_id=X` — en vez de `/projects/{project_id}/test-cases`
- `POST /projects/{project_id}/test-cases` — se mantiene anidado para crear (necesita FK)
- `GET /test-cases/{id}/runs` — mantener, pero la response del run usa la nueva estructura (verdict_reason, steps_json, findings_json)

---

## Resumen de impacto

| Área | Cambio | Impacto |
|------|--------|---------|
| Modelo Project | Agregar `is_active` | Bajo |
| Modelo Run | Separar `verdict_reason`, renombrar `findings_json`, agregar `steps_json` | Medio — cambia el parsing del output del agente |
| API | 2 endpoints nuevos, 1 modificado | Bajo |
| Navegación | Proyecto como contexto global, no nivel de drill-down | Simplifica frontend, cambia la estructura de router |
| Frontend | 3 vistas en vez de 4 | Reduce complejidad |

Estos cambios deben integrarse en `PHASE-1.md` bloques 1.2 (modelo de datos) y 1.4 (frontend) antes de empezar a implementar.
