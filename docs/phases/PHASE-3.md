# Fase 3 — Descubrimiento autónomo

> **Objetivo:** Que el agente explore una app, mapee flujos y proponga test cases.

## Prerequisito

Fase 2 validada. Memory y replay funcionan de forma confiable.

## Estado

**No planificada en detalle.** Este documento se completará cuando la Fase 2 esté validada y en uso.

## Dirección general

### Capacidades esperadas

1. **Discovery mode** — Dado un proyecto (URL + credenciales + descripción), el agente:
   - Navega la app de forma exploratoria
   - Identifica flujos principales (login, navegación, CRUD, etc.)
   - Mapea rutas y pantallas
   - Propone test cases con instrucciones y expected outcomes

2. **Coverage map** — Visualización de:
   - Qué partes de la app están cubiertas por tests
   - Qué rutas/pantallas no tienen cobertura
   - Porcentaje de cobertura estimado

3. **Negative test generation** — Dado un test case positivo:
   - Generar variantes negativas automáticamente
   - "Login exitoso" → "Contraseña incorrecta", "Email vacío", "Email inválido"
   - El usuario revisa y aprueba antes de activar

4. **Suite execution** — Ejecutar múltiples tests:
   - Todos los tests de un proyecto
   - Tests filtrados por tag
   - Ejecución secuencial o paralela (configurable)

## Preguntas abiertas (a resolver cuando se planifique)

- ¿Cómo limitar el costo de una exploración abierta?
- ¿Cómo evitar que el agente genere tests redundantes?
- ¿Cuánto contexto de la app necesita el agente para proponer tests útiles?
- ¿El discovery debería ser un proceso iterativo (varias sesiones) o un solo run largo?
