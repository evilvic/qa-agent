<script setup>
import { ref } from 'vue'

/**
 * TechnicalDetails
 *
 * Información técnica para debugging. Colapsado por defecto.
 * Lo técnico se esconde hasta que se necesita.
 *
 * Props:
 *   model     — Modelo LLM usado
 *   tokens    — Tokens consumidos
 *   duration  — Duración en segundos
 *   url       — URL final
 *   runId     — Identificador del run
 */
defineProps({
  model:    { type: String, default: '' },
  tokens:   { type: Number, default: 0 },
  duration: { type: Number, default: 0 },
  url:      { type: String, default: '' },
  runId:    { type: String, default: '' },
})

const expanded = ref(false)
</script>

<template>
  <div class="tech-details">
    <button
      class="tech-details__toggle"
      :aria-expanded="expanded"
      @click="expanded = !expanded"
    >
      <span class="tech-details__arrow" :class="{ 'tech-details__arrow--open': expanded }">&#9654;</span>
      Detalles técnicos
    </button>
    <Transition name="details">
      <div v-if="expanded" class="tech-details__content">
        <dl class="tech-details__list">
          <div v-if="model" class="tech-details__item">
            <dt>Modelo</dt>
            <dd>{{ model }}</dd>
          </div>
          <div v-if="tokens" class="tech-details__item">
            <dt>Tokens</dt>
            <dd>{{ tokens.toLocaleString('es-MX') }}</dd>
          </div>
          <div v-if="duration" class="tech-details__item">
            <dt>Duración</dt>
            <dd>{{ duration.toFixed(1) }}s</dd>
          </div>
          <div v-if="url" class="tech-details__item">
            <dt>URL final</dt>
            <dd class="tech-details__url">{{ url }}</dd>
          </div>
          <div v-if="runId" class="tech-details__item">
            <dt>Run ID</dt>
            <dd><code>{{ runId }}</code></dd>
          </div>
        </dl>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.tech-details {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.tech-details__toggle {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: var(--surface-section);
  border: none;
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
  cursor: pointer;
  transition: color var(--transition-fast);
  text-align: left;
}

.tech-details__toggle:hover {
  color: var(--text-primary);
}

.tech-details__arrow {
  font-size: 10px;
  transition: transform var(--transition-fast);
}

.tech-details__arrow--open {
  transform: rotate(90deg);
}

.tech-details__content {
  padding: var(--space-4);
  border-top: 1px solid var(--border-default);
}

.tech-details__list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--space-3);
}

.tech-details__item dt {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  margin-bottom: 2px;
}

.tech-details__item dd {
  font-size: var(--font-size-sm);
  color: var(--text-primary);
}

.tech-details__url {
  word-break: break-all;
  font-size: var(--font-size-xs);
}

code {
  font-size: var(--font-size-xs);
  background: var(--surface-section);
  padding: 1px var(--space-1);
  border-radius: var(--radius-sm);
}

/* Transición */
.details-enter-active { animation: fadeIn var(--transition-fast); }
.details-leave-active { transition: opacity var(--transition-fast); }
.details-leave-to     { opacity: 0; }
</style>
