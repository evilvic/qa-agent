<script setup>
/**
 * EmptyState
 *
 * Cada estado vacío es una invitación, no un error.
 * Guía al usuario hacia la siguiente acción.
 *
 * Props:
 *   title       — Título descriptivo
 *   description — Texto de ayuda
 *   actionLabel — Texto del botón (opcional, si hay acción)
 *
 * Emits:
 *   action — Cuando el usuario clickea el botón
 */
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  actionLabel: { type: String, default: '' },
})

defineEmits(['action'])
</script>

<template>
  <div class="empty-state">
    <div class="empty-state__content">
      <h3 class="empty-state__title">{{ title }}</h3>
      <p v-if="description" class="empty-state__description">{{ description }}</p>
      <button
        v-if="actionLabel"
        class="empty-state__action"
        @click="$emit('action')"
      >
        {{ actionLabel }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-12) var(--space-6);
  text-align: center;
}

.empty-state__content {
  max-width: 400px;
}

.empty-state__title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.empty-state__description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
  margin-bottom: var(--space-6);
}

.empty-state__action {
  display: inline-flex;
  padding: var(--space-2) var(--space-6);
  background: var(--action-primary);
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.empty-state__action:hover {
  background: var(--action-primary-hover);
}

.empty-state__action:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--action-focus-ring);
}
</style>
