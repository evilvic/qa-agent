# Fase 1 — Core estable + Test Cases

> **Objetivo:** Que el sistema funcione de forma confiable y los test cases persistan con veredicto pass/fail.

## Prerequisito

Ninguno. Esta es la base.

## Criterio de salida

- [ ] Puedo crear test cases desde el frontend
- [ ] Puedo ejecutar un test case y ver el resultado pass/fail con evidencia
- [ ] Si un run falla (timeout, error de browser, error de LLM), recibo un error claro, no un spinner infinito
- [ ] Los runs persisten en base de datos. Puedo cerrar el browser y volver a ver resultados anteriores
- [ ] Los artifacts (screenshots, video) se asocian al run y son accesibles desde el frontend

---

## Bloque 1.1 — Estabilización del backend

**Objetivo:** Que `POST /run` nunca se cuelgue, nunca crashee silenciosamente, y siempre retorne un resultado o error claro.

### Tareas

#### 1.1.1 Timeout en agent.run()
- Wrap `agent.run()` con `asyncio.wait_for(timeout=120)`
- Si timeout: matar browser, retornar error estructurado
- El timeout debe ser configurable via env var `AGENT_TIMEOUT` (default: 120s)

#### 1.1.2 Error handling completo en /run
- Try/except alrededor de todo el bloque del agente
- Capturar errores de: browser launch, navegación, LLM API, parsing de resultado
- Siempre retornar un response estructurado (agregar campo `error` al modelo)
- Nunca retornar HTTP 500 genérico

#### 1.1.3 Structured logging
- Configurar `logging` con formato JSON
- Logs obligatorios: inicio de run, steps del agente, resultado, errores
- Nivel INFO para flujo normal, ERROR para fallos
- Log de tokens/modelo usado por run (para tracking de costos)

#### 1.1.4 Pinear dependencies
- `pip freeze` → requirements.txt con versiones exactas
- Documentar versión de Python requerida

#### 1.1.5 Extraer prompt a módulo
- Mover `_make_task()` a `backend/prompt.py`
- Importar desde main.py y desde tests
- Eliminar prompt duplicado en test_login_describe.py

#### 1.1.6 Validar env vars al startup
- Verificar required vars cuando arranca FastAPI (evento `startup`)
- Si faltan, log de error claro y exit (no esperar al primer request)

#### 1.1.7 Eliminar referencias hardcoded a apps específicas
- El prompt no debe asumir una app target fija
- Las credenciales y URL vienen del modelo de datos (Project), no solo de env vars

### Entregable
Backend que ejecuta runs de forma confiable, con errores claros y logging.

---

## Bloque 1.2 — Modelo de datos y persistencia

**Objetivo:** Test cases y runs persisten en SQLite.

### Tareas

#### 1.2.1 Setup de base de datos
- Librería: SQLModel (Pydantic + SQLAlchemy, compatible con FastAPI)
- Base de datos: SQLite, archivo en `backend/data/qa_agent.db`
- Migraciones: no necesarias en MVP, schema se crea al iniciar

#### 1.2.2 Modelo Project
```
projects
├── id: str (uuid)
├── name: str
├── base_url: str
├── login_path: str | null
├── credentials_email: str
├── credentials_password: str (encrypted at rest)
├── description: str | null
├── viewport_width: int (default 390)
├── viewport_height: int (default 844)
├── created_at: datetime
└── updated_at: datetime
```

#### 1.2.3 Modelo TestCase
```
test_cases
├── id: str (uuid)
├── project_id: str (FK → projects)
├── name: str
├── instructions: str
├── expected_outcome: str
├── tags: str | null (comma-separated)
├── is_active: bool (default true)
├── created_at: datetime
└── updated_at: datetime
```

#### 1.2.4 Modelo Run
```
runs
├── id: str (uuid)
├── test_case_id: str (FK → test_cases)
├── status: str (running | pass | fail | error)
├── screen_json: str | null (JSON)
├── task_result_json: str | null (JSON)
├── execution_path_json: str | null (JSON) — lo que hizo el agente
├── error_message: str | null
├── model_used: str
├── tokens_used: int | null
├── elapsed_ms: int | null
├── artifacts_path: str | null
├── created_at: datetime
└── finished_at: datetime | null
```

#### 1.2.5 Endpoints CRUD

**Projects:**
- `POST /projects` — crear proyecto
- `GET /projects` — listar proyectos
- `GET /projects/{id}` — detalle
- `PUT /projects/{id}` — editar
- `DELETE /projects/{id}` — borrar

**Test Cases:**
- `POST /projects/{project_id}/test-cases` — crear test case
- `GET /projects/{project_id}/test-cases` — listar test cases del proyecto
- `GET /test-cases/{id}` — detalle
- `PUT /test-cases/{id}` — editar
- `DELETE /test-cases/{id}` — borrar

**Runs:**
- `POST /test-cases/{id}/run` — ejecutar test case (reemplaza POST /run actual)
- `GET /test-cases/{id}/runs` — historial de runs de un test case
- `GET /runs/{id}` — detalle de un run con artifacts

**Health:**
- `GET /healthz` — mantener, agregar check de DB

### Entregable
API REST completa con persistencia en SQLite.

---

## Bloque 1.3 — Lógica de pass/fail

**Objetivo:** Cada run produce un veredicto claro: PASS, FAIL, o ERROR con explicación.

### Tareas

#### 1.3.1 Modificar el prompt del agente
- Agregar al prompt el `expected_outcome` del test case
- Pedir al agente que evalúe: "¿El resultado obtenido coincide con lo esperado?"
- Formato de respuesta del agente debe incluir:
  - `verdict`: "pass" | "fail"
  - `reason`: explicación en español de por qué pasó o falló
  - `evidence`: qué observó en la pantalla que sustenta el veredicto

#### 1.3.2 Parsing del veredicto
- Extraer verdict/reason/evidence del output del agente
- Si el agente no retorna veredicto claro, marcar como ERROR
- Guardar en la tabla runs

#### 1.3.3 Manejo de errores como status
- Timeout → status: error, error_message: "Timeout después de Xs"
- Browser crash → status: error, error_message descriptivo
- LLM error → status: error, error_message descriptivo
- Estos NO son "fail" (fail es cuando el test se ejecutó pero el resultado no fue el esperado)

### Entregable
Cada run tiene veredicto pass/fail/error con explicación legible.

---

## Bloque 1.4 — Frontend para test cases

**Objetivo:** UI funcional para crear, ejecutar y revisar test cases.

> **Nota:** Este bloque se trabajará con /experience-architect para definir la experiencia antes de implementar.

### Vistas necesarias (funcional, no diseño final)

#### Vista: Lista de proyectos
- Lista de proyectos con nombre y URL
- Botón crear proyecto
- Click en proyecto → ver sus test cases

#### Vista: Test cases de un proyecto
- Lista de test cases con nombre, último resultado (pass/fail/error/sin ejecutar)
- Botón crear test case
- Botón ejecutar en cada test case
- Click en test case → ver historial de runs

#### Vista: Historial de runs de un test case
- Lista de runs con: fecha, status (pass/fail/error), duración
- Click en run → ver detalle

#### Vista: Detalle de un run
- Status pass/fail/error con razón
- Screenshots en grid
- Screen info (URL, título, elementos)
- Task result
- Tiempo de ejecución, modelo usado

### Entregable
Frontend funcional que permite el flujo completo: crear proyecto → crear test → ejecutar → ver resultado.

---

## Estimación de esfuerzo

| Bloque | Esfuerzo estimado |
|--------|-------------------|
| 1.1 Estabilización backend | Medio |
| 1.2 Modelo de datos + endpoints | Alto |
| 1.3 Lógica pass/fail | Medio |
| 1.4 Frontend test cases | Alto (incluye diseño de experiencia) |

## Orden de ejecución

```
1.1 (estabilización) → 1.2 (datos + API) → 1.3 (pass/fail) → 1.4 (frontend)
```

Cada bloque se puede validar independientemente antes de avanzar al siguiente.
