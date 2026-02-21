<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

/**
 * RunningIndicator
 *
 * Feedback persistente cuando hay un run activo.
 * Barra fija en la parte inferior. Siempre visible mientras haya un run.
 * Reduce la ansiedad de la espera mostrando que algo está pasando.
 *
 * Props:
 *   testName  — Nombre del test en ejecución
 *   startTime — Timestamp de inicio (para calcular elapsed)
 *   visible   — Controla si se muestra
 *
 * Emits:
 *   navigate — Cuando el usuario quiere ir al test que está corriendo
 */
const props = defineProps({
  testName: { type: String, default: '' },
  startTime: { type: Number, default: 0 },
  visible: { type: Boolean, default: false },
})

defineEmits(['navigate'])

const elapsed = ref(0)
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    if (props.startTime) {
      elapsed.value = Math.floor((Date.now() - props.startTime) / 1000)
    }
  }, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<template>
  <Transition name="indicator">
    <div v-if="visible" class="running-indicator" role="status" aria-live="polite">
      <div class="running-indicator__content">
        <span class="running-indicator__dot" aria-hidden="true"></span>
        <span class="running-indicator__text">
          Ejecutando
          <strong v-if="testName">"{{ testName }}"</strong>
          <template v-if="elapsed > 0"> — {{ elapsed }}s</template>
        </span>
        <button class="running-indicator__link" @click="$emit('navigate')">
          Ver
        </button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.running-indicator {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--color-running-bg);
  border-top: 1px solid var(--color-running-border);
  padding: var(--space-3) var(--space-4);
  z-index: 100;
}

.running-indicator__content {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  max-width: var(--content-max-width);
  margin: 0 auto;
  font-size: var(--font-size-sm);
  color: var(--color-running-text);
}

.running-indicator__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-running);
  animation: pulse 1.5s ease-in-out infinite;
  flex-shrink: 0;
}

.running-indicator__text {
  flex: 1;
}

.running-indicator__link {
  background: none;
  border: 1px solid var(--color-running-border);
  border-radius: var(--radius-md);
  padding: 2px var(--space-3);
  color: var(--color-running-text);
  font-family: var(--font-family);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.running-indicator__link:hover {
  background: rgba(59, 130, 246, 0.1);
}

/* Transición de entrada/salida */
.indicator-enter-active { animation: fadeIn var(--transition-normal); }
.indicator-leave-active { transition: opacity var(--transition-fast), transform var(--transition-fast); }
.indicator-leave-to     { opacity: 0; transform: translateY(8px); }
</style>
