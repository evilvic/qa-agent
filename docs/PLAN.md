# Plan maestro de ejecución

> De proof-of-concept a producto de QA autónomo con memoria.

## Visión en una línea

Un sistema donde describes qué quieres probar, el agente lo ejecuta, recuerda cómo lo hizo, y con el tiempo propone qué más probar.

## Fases

| Fase | Nombre | Objetivo | Dependencia | Detalle |
|------|--------|----------|-------------|---------|
| **1** | Core estable + Test Cases | Que el sistema funcione sin colgarse y los tests persistan | Ninguna | [PHASE-1.md](phases/PHASE-1.md) |
| **2** | Memory + Replay inteligente | Que el segundo run sea más rápido y barato | Fase 1 completa | [PHASE-2.md](phases/PHASE-2.md) |
| **3** | Descubrimiento autónomo | Que el agente explore y proponga tests | Fase 2 validada | [PHASE-3.md](phases/PHASE-3.md) (pendiente) |
| **4** | Producto desplegable | Auth, deploy, multi-tenant | Fase 3 funcional | No planificada |

## Modelo de dominio

```
Project (app target)
  ├── name, base_url, login_path, credentials, description
  │
  └── Test Cases
       ├── name, instructions, expected_outcome, tags
       │
       ├── Runs (ejecuciones)
       │    ├── status: pass | fail | error
       │    ├── screen_json, task_result_json
       │    ├── error_message, elapsed_ms
       │    ├── artifacts_path (screenshots, video, traces)
       │    ├── model_used, tokens_used
       │    └── execution_path_json (lo que hizo el agente)
       │
       └── Memory (conocimiento acumulado)
            ├── execution_path_json (path exitoso más reciente)
            ├── created_from_run_id
            ├── success_count (veces que funcionó)
            └── last_used_at
```

## Conceptos clave

### Test Case vs Run
- **Test Case** = QUE quieres probar (persiste, se re-ejecuta)
- **Run** = UNA ejecución de un test case (resultado histórico)

### Memory
- Se crea automáticamente después de un run exitoso
- Contiene el execution path (selectores, clicks, navegación)
- Se inyecta en el prompt del siguiente run como contexto
- Si el replay falla, el agente redescubre y actualiza la memory

### Model routing
- Sin memory → modelo capaz (descubrimiento)
- Con memory → modelo barato (replay)
- Replay falla → escalar a modelo capaz

### Pass/Fail
- Evaluado por el LLM comparando resultado vs expected_outcome
- No es assertion exacta, es evaluación semántica
- El agente debe explicar POR QUE pasó o falló

## Señales de éxito por fase

| Fase | Señal |
|------|-------|
| 1 | 10 test cases creados, ejecutados, con historial persistente y veredicto pass/fail |
| 2 | Segundo run de un test es >50% más rápido y usa menos tokens que el primero |
| 3 | El agente propone 5+ test cases válidos a partir de explorar una app nueva |
| 4 | Otro usuario puede registrarse, configurar su app, y correr tests sin ayuda |

## Kill criteria

- Si >50% de los runs fallan consistentemente por problemas del agente (no de la app) → revisar viabilidad del approach
- Si el costo promedio por run supera $0.50 → el modelo económico no cierra
- Si después de Fase 1 completa, el sistema no se usa semanalmente → el problema no es automatización

## Documentación del sistema

| Archivo | Propósito |
|---------|-----------|
| `docs/PLAN.md` | Este archivo. Plan maestro con fases y modelo de dominio |
| `docs/CONTEXT.md` | Contexto del producto, visión, competidor, principios |
| `docs/DECISIONS.md` | Log de decisiones con trade-offs |
| `docs/PROGRESS.md` | Log cronológico de avances y bloqueos |
| `docs/phases/PHASE-N.md` | Detalle de cada fase con tareas, criterios y entregables |
| `CLAUDE.md` | Guía técnica para el agente de código |
