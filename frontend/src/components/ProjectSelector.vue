<script setup>
import { ref } from 'vue'

/**
 * ProjectSelector
 *
 * Dropdown para cambiar de proyecto (app target) sin navegar.
 * Cambiar de proyecto es como cambiar de workspace.
 *
 * Props:
 *   projects      — Array de { id, name }
 *   activeId      — ID del proyecto activo
 *
 * Emits:
 *   select — ID del proyecto seleccionado
 *   create — Cuando el usuario quiere crear un nuevo proyecto
 */
defineProps({
  projects: { type: Array, default: () => [] },
  activeId: { type: String, default: '' },
})

defineEmits(['select', 'create'])

const open = ref(false)

function toggle() {
  open.value = !open.value
}

function close() {
  open.value = false
}
</script>

<template>
  <div class="project-selector" v-if="projects.length > 0">
    <button
      class="project-selector__trigger"
      :aria-expanded="open"
      @click="toggle"
      @blur="close"
    >
      <span class="project-selector__name">
        {{ projects.find(p => p.id === activeId)?.name || 'Seleccionar proyecto' }}
      </span>
      <span class="project-selector__chevron" :class="{ 'project-selector__chevron--open': open }">&#9662;</span>
    </button>
    <Transition name="dropdown">
      <div v-if="open" class="project-selector__menu" role="listbox">
        <button
          v-for="project in projects"
          :key="project.id"
          class="project-selector__option"
          :class="{ 'project-selector__option--active': project.id === activeId }"
          role="option"
          :aria-selected="project.id === activeId"
          @mousedown.prevent="$emit('select', project.id); close()"
        >
          <span v-if="project.id === activeId" class="project-selector__check">&#10003;</span>
          <span v-else class="project-selector__check">&nbsp;</span>
          {{ project.name }}
        </button>
        <div class="project-selector__divider"></div>
        <button
          class="project-selector__option project-selector__option--create"
          @mousedown.prevent="$emit('create'); close()"
        >
          + Nuevo proyecto
        </button>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.project-selector {
  position: relative;
}

.project-selector__trigger {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-3);
  background: none;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  cursor: pointer;
  transition: border-color var(--transition-fast);
}

.project-selector__trigger:hover {
  border-color: var(--border-hover);
}

.project-selector__chevron {
  font-size: 10px;
  transition: transform var(--transition-fast);
}

.project-selector__chevron--open {
  transform: rotate(180deg);
}

.project-selector__menu {
  position: absolute;
  top: calc(100% + 4px);
  right: 0;
  min-width: 220px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  z-index: 50;
}

.project-selector__option {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  width: 100%;
  padding: var(--space-2) var(--space-3);
  background: none;
  border: none;
  font-family: var(--font-family);
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  cursor: pointer;
  text-align: left;
  transition: background var(--transition-fast);
}

.project-selector__option:hover {
  background: var(--surface-section);
}

.project-selector__option--active {
  font-weight: var(--font-weight-medium);
}

.project-selector__option--create {
  color: var(--action-primary);
  font-weight: var(--font-weight-medium);
}

.project-selector__check {
  width: 16px;
  font-size: var(--font-size-xs);
  color: var(--action-primary);
}

.project-selector__divider {
  height: 1px;
  background: var(--border-default);
  margin: var(--space-1) 0;
}

/* Transición */
.dropdown-enter-active { animation: fadeIn var(--transition-fast); }
.dropdown-leave-active { transition: opacity var(--transition-fast); }
.dropdown-leave-to     { opacity: 0; }
</style>
