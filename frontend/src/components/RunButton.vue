<script setup>
/**
 * RunButton
 *
 * Dispara la ejecución de un test case.
 * Tres estados: idle (listo), running (en progreso), disabled (no disponible).
 *
 * Props:
 *   state    — 'idle' | 'running' | 'disabled'
 *   compact  — Si true, muestra solo ícono (para uso en listas)
 *
 * Emits:
 *   run — Cuando el usuario clickea para ejecutar
 */
defineProps({
  state: {
    type: String,
    default: 'idle',
    validator: (v) => ['idle', 'running', 'disabled'].includes(v),
  },
  compact: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['run'])
</script>

<template>
  <button
    class="run-button"
    :class="[
      `run-button--${state}`,
      { 'run-button--compact': compact }
    ]"
    :disabled="state !== 'idle'"
    :aria-label="state === 'running' ? 'Ejecutando prueba' : 'Ejecutar prueba'"
    @click="$emit('run')"
  >
    <span v-if="state === 'running'" class="run-button__spinner" aria-hidden="true"></span>
    <span v-else-if="compact" class="run-button__icon" aria-hidden="true">&#9654;</span>
    <template v-if="!compact">
      {{ state === 'running' ? 'Ejecutando\u2026' : 'Ejecutar' }}
    </template>
  </button>
</template>

<style scoped>
.run-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: background var(--transition-fast), box-shadow var(--transition-fast);
  line-height: var(--line-height-tight);
}

.run-button--idle {
  background: var(--action-primary);
  color: var(--text-inverse);
}

.run-button--idle:hover {
  background: var(--action-primary-hover);
}

.run-button--idle:active {
  background: var(--action-primary-active);
}

.run-button--idle:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--action-focus-ring);
}

.run-button--running {
  background: var(--color-running-bg);
  color: var(--color-running-text);
  cursor: not-allowed;
}

.run-button--disabled {
  background: var(--color-neutral-bg);
  color: var(--text-disabled);
  cursor: not-allowed;
  border: 1px solid var(--border-default);
}

.run-button--compact {
  padding: var(--space-1) var(--space-2);
  min-width: 32px;
  min-height: 32px;
}

.run-button__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--color-running-border);
  border-top-color: var(--color-running);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.run-button__icon {
  font-size: 10px;
}
</style>
