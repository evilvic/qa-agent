# Fase 2 — Memory + Replay inteligente

> **Objetivo:** Que el segundo run de un test case sea más rápido y barato que el primero.

## Prerequisito

Fase 1 completa. Test cases y runs funcionan con veredicto pass/fail.

## Criterio de salida

- [ ] Después de un run exitoso, se guarda automáticamente el execution path
- [ ] Al re-ejecutar un test case, el agente recibe el path anterior como contexto
- [ ] El segundo run usa un modelo más barato que el primero
- [ ] Si el replay falla (algo cambió en la app), el agente escala a descubrimiento automáticamente
- [ ] La memory se actualiza cuando el agente encuentra un nuevo path exitoso
- [ ] Se puede ver en el frontend si un run usó memory o no, y el modelo/costo

---

## Bloque 2.1 — Captura de execution path

### Tareas

#### 2.1.1 Extraer execution path del historial del agente
- Después de `agent.run()`, extraer del `history`:
  - Secuencia de acciones (click, type, navigate, wait)
  - Selectores usados para cada acción
  - URLs visitadas en orden
  - Texto ingresado (sin contraseñas)
- Formato JSON estructurado

#### 2.1.2 Modelo Memory en base de datos
```
memories
├── id: str (uuid)
├── test_case_id: str (FK → test_cases, unique)
├── execution_path_json: str (JSON del path)
├── created_from_run_id: str (FK → runs)
├── success_count: int (veces que el path funcionó)
├── fail_count: int (veces que falló y se redescubrió)
├── last_used_at: datetime
├── created_at: datetime
└── updated_at: datetime
```

#### 2.1.3 Guardar memory automáticamente
- Después de un run con status "pass":
  - Si no hay memory para ese test case → crear
  - Si hay memory y el path cambió → actualizar
  - Si hay memory y el path es el mismo → incrementar success_count

### Entregable
Cada run exitoso deja un execution path guardado.

---

## Bloque 2.2 — Replay con memory

### Tareas

#### 2.2.1 Inyectar memory en el prompt
- Si existe memory para el test case, agregar al prompt:
  ```
  CONTEXTO DE EJECUCIÓN ANTERIOR:
  La última vez que esta prueba fue exitosa, seguiste estos pasos:
  [execution_path formateado]

  Intenta seguir el mismo camino. Si algo no funciona como se esperaba
  (un botón cambió, un selector no existe, la página se ve diferente),
  entonces explora para encontrar la nueva ruta y reporta qué cambió.
  ```

#### 2.2.2 Model routing
- Lógica de selección de modelo:
  ```
  Si hay memory con success_count >= 2:
    → usar modelo barato (gpt-4.1-mini o nano)
    → max_steps reducido (la mitad del default)
  Si hay memory con success_count < 2:
    → usar modelo standard (gpt-4.1-mini)
    → max_steps normal
  Si NO hay memory:
    → usar modelo capaz (gpt-4.1)
    → max_steps normal o aumentado
  ```
- El modelo usado se guarda en el run (`model_used`)
- Configurable via env vars: `MODEL_DISCOVERY`, `MODEL_REPLAY`, `MODEL_CHEAP_REPLAY`

#### 2.2.3 Escalamiento automático
- Si un run con memory falla (status: fail o error):
  - Re-intentar automáticamente con modelo más capaz
  - Marcar el run original como "replay_failed"
  - El nuevo run se ejecuta en modo descubrimiento
  - Si el nuevo run pasa → actualizar memory con nuevo path

#### 2.2.4 Tracking de costos
- Guardar `tokens_used` por run
- Calcular costo estimado (basado en pricing del modelo)
- Endpoint: `GET /projects/{id}/stats` → tokens totales, costo estimado, runs por status

### Entregable
El segundo run de un test case es notablemente más rápido/barato. El agente se adapta automáticamente cuando la app cambia.

---

## Bloque 2.3 — Visibilidad de memory en frontend

### Tareas

#### 2.3.1 Indicadores en UI
- En la lista de test cases: badge "tiene memory" vs "sin memory"
- En el detalle del run: mostrar si usó memory o no
- En el detalle del run: modelo usado y tokens consumidos

#### 2.3.2 Vista de memory
- En el detalle del test case: ver el execution path guardado
- Opción de "borrar memory" (forzar redescubrimiento)

#### 2.3.3 Dashboard de costos
- Vista simple con: runs totales, tokens totales, costo estimado
- Breakdown por test case

### Entregable
El usuario puede ver cómo la memory afecta el rendimiento y costo de sus tests.

---

## Riesgos específicos de esta fase

| Riesgo | Mitigación |
|--------|------------|
| `browser_use` no expone suficiente detalle del execution path | Investigar API de history antes de empezar. Si no es viable, capturar a nivel de prompt (pedir al agente que reporte sus pasos). |
| Memory desactualizada causa más fallos que aciertos | Implementar "confidence score". Si fail_count > success_count, borrar memory. |
| Escalamiento automático duplica costos en runs fallidos | Limit de 1 re-intento. Si falla dos veces, marcar como error definitivo. |

## Orden de ejecución

```
2.1 (captura de path) → 2.2 (replay + routing) → 2.3 (UI)
```
