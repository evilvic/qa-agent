<script setup>
import { ref, watch } from 'vue'

/**
 * TestForm
 *
 * Crear o editar un test case. Inline, no nueva página.
 * Tres campos separados porque cada uno tiene un propósito distinto:
 *   nombre       → para la lista (identificar rápido)
 *   instrucciones → para el agente (qué hacer)
 *   resultado esperado → para el veredicto (cómo evaluar)
 *
 * Props:
 *   initialName         — Nombre pre-poblado (modo edición)
 *   initialInstructions — Instrucciones pre-pobladas
 *   initialExpected     — Resultado esperado pre-poblado
 *   saving              — Si está guardando (deshabilita form)
 *
 * Emits:
 *   save   — { name, instructions, expected }
 *   cancel — Cuando el usuario cancela
 */
const props = defineProps({
  initialName:         { type: String, default: '' },
  initialInstructions: { type: String, default: '' },
  initialExpected:     { type: String, default: '' },
  saving:              { type: Boolean, default: false },
})

const emit = defineEmits(['save', 'cancel'])

const name = ref(props.initialName)
const instructions = ref(props.initialInstructions)
const expected = ref(props.initialExpected)
const errors = ref({})

watch(() => props.initialName, (v) => { name.value = v })
watch(() => props.initialInstructions, (v) => { instructions.value = v })
watch(() => props.initialExpected, (v) => { expected.value = v })

function validate() {
  errors.value = {}
  if (!name.value.trim()) errors.value.name = 'El nombre es obligatorio'
  if (!instructions.value.trim()) errors.value.instructions = 'Las instrucciones son obligatorias'
  if (!expected.value.trim()) errors.value.expected = 'El resultado esperado es obligatorio'
  return Object.keys(errors.value).length === 0
}

function handleSave() {
  if (!validate()) return
  emit('save', {
    name: name.value.trim(),
    instructions: instructions.value.trim(),
    expected: expected.value.trim(),
  })
}
</script>

<template>
  <form class="test-form" @submit.prevent="handleSave">
    <div class="test-form__field" :class="{ 'test-form__field--error': errors.name }">
      <label class="test-form__label" for="tf-name">Nombre</label>
      <input
        id="tf-name"
        v-model="name"
        type="text"
        class="test-form__input"
        placeholder="Login con credenciales válidas"
        maxlength="100"
        :disabled="saving"
      />
      <span v-if="errors.name" class="test-form__error">{{ errors.name }}</span>
    </div>

    <div class="test-form__field" :class="{ 'test-form__field--error': errors.instructions }">
      <label class="test-form__label" for="tf-instructions">Instrucciones</label>
      <textarea
        id="tf-instructions"
        v-model="instructions"
        class="test-form__textarea"
        placeholder="Inicia sesión con las credenciales del proyecto y navega al dashboard."
        rows="3"
        :disabled="saving"
      ></textarea>
      <span class="test-form__helper">Describe qué quieres probar. El agente descubrirá cómo hacerlo.</span>
      <span v-if="errors.instructions" class="test-form__error">{{ errors.instructions }}</span>
    </div>

    <div class="test-form__field" :class="{ 'test-form__field--error': errors.expected }">
      <label class="test-form__label" for="tf-expected">Resultado esperado</label>
      <textarea
        id="tf-expected"
        v-model="expected"
        class="test-form__textarea"
        placeholder="El dashboard se muestra con el nombre del usuario visible."
        rows="2"
        :disabled="saving"
      ></textarea>
      <span class="test-form__helper">¿Cómo sabes si la prueba pasó? ¿Qué debería verse en pantalla?</span>
      <span v-if="errors.expected" class="test-form__error">{{ errors.expected }}</span>
    </div>

    <div class="test-form__actions">
      <button
        type="submit"
        class="test-form__save"
        :disabled="saving"
      >
        <span v-if="saving" class="test-form__spinner"></span>
        {{ saving ? 'Guardando\u2026' : 'Guardar' }}
      </button>
      <button
        type="button"
        class="test-form__cancel"
        :disabled="saving"
        @click="$emit('cancel')"
      >
        Cancelar
      </button>
    </div>
  </form>
</template>

<style scoped>
.test-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--surface-card);
  animation: fadeIn var(--transition-normal);
}

.test-form__label {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.test-form__input,
.test-form__textarea {
  display: block;
  width: 100%;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  background: var(--surface-card);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  resize: vertical;
}

.test-form__input:focus,
.test-form__textarea:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px var(--action-focus-ring);
}

.test-form__field--error .test-form__input,
.test-form__field--error .test-form__textarea {
  border-color: var(--color-fail);
}

.test-form__field--error .test-form__input:focus,
.test-form__field--error .test-form__textarea:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}

.test-form__helper {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  margin-top: var(--space-1);
}

.test-form__error {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--color-fail-text);
  margin-top: var(--space-1);
}

.test-form__actions {
  display: flex;
  gap: var(--space-2);
}

.test-form__save {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
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

.test-form__save:hover:not(:disabled) { background: var(--action-primary-hover); }
.test-form__save:disabled { opacity: 0.6; cursor: not-allowed; }

.test-form__cancel {
  padding: var(--space-2) var(--space-4);
  background: none;
  color: var(--text-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: border-color var(--transition-fast), color var(--transition-fast);
}

.test-form__cancel:hover:not(:disabled) {
  border-color: var(--border-hover);
  color: var(--text-primary);
}

.test-form__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: var(--text-inverse);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
</style>
