<script setup>
/**
 * StatusBadge
 *
 * Indicador visual del estado de un run. Componente atómico reutilizable.
 * Un badge verde SIEMPRE significa "pasó". No hay reinterpretación por contexto.
 *
 * Props:
 *   status — 'pass' | 'fail' | 'error' | 'running' | 'none'
 */
const props = defineProps({
  status: {
    type: String,
    default: 'none',
    validator: (v) => ['pass', 'fail', 'error', 'running', 'none'].includes(v),
  },
})

const labels = {
  pass: 'Pasó',
  fail: 'Falló',
  error: 'Error',
  running: 'Ejecutando\u2026',
  none: 'Sin ejecutar',
}
</script>

<template>
  <span
    class="status-badge"
    :class="`status-badge--${status}`"
    role="status"
    :aria-label="labels[status]"
  >
    <span v-if="status === 'running'" class="status-badge__dot" aria-hidden="true"></span>
    {{ labels[status] }}
  </span>
</template>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-tight);
  border: 1px solid;
  white-space: nowrap;
  user-select: none;
}

.status-badge--pass {
  background: var(--color-pass-bg);
  border-color: var(--color-pass-border);
  color: var(--color-pass-text);
}

.status-badge--fail {
  background: var(--color-fail-bg);
  border-color: var(--color-fail-border);
  color: var(--color-fail-text);
}

.status-badge--error {
  background: var(--color-error-bg);
  border-color: var(--color-error-border);
  color: var(--color-error-text);
}

.status-badge--running {
  background: var(--color-running-bg);
  border-color: var(--color-running-border);
  color: var(--color-running-text);
  animation: pulse 2s ease-in-out infinite;
}

.status-badge--none {
  background: var(--color-neutral-bg);
  border-color: var(--color-neutral-border);
  color: var(--color-neutral-text);
}

.status-badge__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-running);
  animation: pulse 1s ease-in-out infinite;
}
</style>
