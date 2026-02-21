<script setup>
/**
 * VerdictCard
 *
 * El momento de verdad: ¿pasó o falló?
 * Siempre es lo primero que el usuario ve después de un run.
 * Borde izquierdo grueso del color del estado. Texto grande y claro.
 *
 * Props:
 *   status — 'pass' | 'fail' | 'error'
 *   reason — Explicación en lenguaje humano
 */
defineProps({
  status: {
    type: String,
    required: true,
    validator: (v) => ['pass', 'fail', 'error'].includes(v),
  },
  reason: {
    type: String,
    default: '',
  },
})

const verdicts = {
  pass: 'Pasó',
  fail: 'Falló',
  error: 'Error',
}
</script>

<template>
  <div
    class="verdict-card"
    :class="`verdict-card--${status}`"
    role="alert"
  >
    <div class="verdict-card__status">
      {{ verdicts[status] }}
    </div>
    <p v-if="reason" class="verdict-card__reason">
      {{ reason }}
    </p>
  </div>
</template>

<style scoped>
.verdict-card {
  padding: var(--space-6);
  border-radius: var(--radius-lg);
  border-left: 4px solid;
  animation: fadeIn var(--transition-normal);
}

.verdict-card--pass {
  background: var(--color-pass-bg);
  border-left-color: var(--color-pass);
}

.verdict-card--fail {
  background: var(--color-fail-bg);
  border-left-color: var(--color-fail);
}

.verdict-card--error {
  background: var(--color-error-bg);
  border-left-color: var(--color-error);
}

.verdict-card__status {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin-bottom: var(--space-2);
}

.verdict-card--pass .verdict-card__status { color: var(--color-pass-text); }
.verdict-card--fail .verdict-card__status { color: var(--color-fail-text); }
.verdict-card--error .verdict-card__status { color: var(--color-error-text); }

.verdict-card__reason {
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
  color: var(--text-primary);
}
</style>
