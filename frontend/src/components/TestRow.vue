<script setup>
import StatusBadge from './StatusBadge.vue'
import RunButton from './RunButton.vue'

/**
 * TestRow
 *
 * Una fila en la lista de tests. Resumen visual rápido.
 * Muestra: badge de estado, nombre, metadata, botón ejecutar.
 *
 * Props:
 *   name      — Nombre del test
 *   status    — Estado del último run
 *   lastRun   — Texto de última ejecución (ej: "hace 2 horas")
 *   running   — Si este test está corriendo ahora
 *
 * Emits:
 *   select — Cuando el usuario clickea para ver detalle
 *   run    — Cuando el usuario clickea para ejecutar
 */
defineProps({
  name:    { type: String, required: true },
  status:  { type: String, default: 'none' },
  lastRun: { type: String, default: '' },
  running: { type: Boolean, default: false },
})

defineEmits(['select', 'run'])
</script>

<template>
  <div
    class="test-row"
    role="listitem"
    @click="$emit('select')"
  >
    <div class="test-row__info">
      <StatusBadge :status="running ? 'running' : status" />
      <div class="test-row__text">
        <span class="test-row__name">{{ name }}</span>
        <span v-if="lastRun" class="test-row__meta">{{ lastRun }}</span>
      </div>
    </div>
    <div class="test-row__actions" @click.stop>
      <RunButton
        compact
        :state="running ? 'running' : 'idle'"
        @run="$emit('run')"
      />
    </div>
  </div>
</template>

<style scoped>
.test-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--surface-card);
  cursor: pointer;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.test-row:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow-sm);
}

.test-row__info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-width: 0;
  flex: 1;
}

.test-row__text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.test-row__name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.test-row__meta {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

.test-row__actions {
  flex-shrink: 0;
  margin-left: var(--space-3);
}
</style>
