<script setup>
import { ref } from 'vue'
import { postQA, getImageUrl } from './api'

const instructions = ref('')
const loading = ref(false)
const error = ref(null)
const result = ref(null)

const handleSubmit = async () => {
  loading.value = true
  error.value = null
  result.value = null
  
  try {
    const response = await postQA(instructions.value)
    result.value = response
  } catch (err) {
    error.value = err.message
  }
  
  loading.value = false
}



const handleImageError = (event) => {
  // Si la imagen no se puede cargar, mostrar un placeholder
  event.target.style.display = 'none'
  const container = event.target.parentElement
  container.innerHTML = '<div class="image-error">Imagen no disponible</div>'
}
</script>

<template>
  <div class="container">
    <h1>🚀 QA Test Client</h1>
    
    <div class="form-section">
      <h2>Configuración del test</h2>
      
      <div class="form-group">
        <label for="instructions">Instrucciones:</label>
        <textarea 
          id="instructions"
          v-model="instructions"
          placeholder="Ingresa las instrucciones para el test..."
          rows="4"
        ></textarea>
      </div>
      

      
      <div class="buttons">
        <button @click="handleSubmit" :disabled="loading || !instructions">
          {{ loading ? 'Ejecutando...' : 'Ejecutar Test' }}
        </button>
        

      </div>
    </div>
    
    <div v-if="error" class="error">
      <h3>❌ Error:</h3>
      <pre>{{ error }}</pre>
    </div>
    
    <div v-if="result" class="result">
      <h3>✅ Resultado del Test</h3>
      
      <!-- Información del test -->
      <div class="test-info">
        <div class="info-item">
          <strong>Run ID:</strong> {{ result.run_id }}
        </div>
        <div class="info-item">
          <strong>URL Final:</strong> {{ result.screen?.url }}
        </div>
        <div class="info-item">
          <strong>Tiempo:</strong> {{ (result.elapsed_ms / 1000).toFixed(2) }}s
        </div>
        <div class="info-item">
          <strong>Pasos:</strong> {{ result.screenshots?.length || 0 }}
        </div>
      </div>
      
      <!-- Grilla de screenshots -->
      <div v-if="result.screenshots && result.screenshots.length > 0" class="screenshots-section">
        <h4>📸 Screenshots del Test</h4>
        <div class="screenshots-grid">
          <div 
            v-for="(screenshot, index) in result.screenshots" 
            :key="index"
            class="screenshot-item"
          >
            <div class="screenshot-header">
              <span class="step-number">Paso {{ index + 1 }}</span>
              <span class="url">{{ result.urls?.[index] || 'N/A' }}</span>
            </div>
            <div class="screenshot-container">
              <img 
                :src="getImageUrl(screenshot)" 
                :alt="`Screenshot paso ${index + 1}`"
                @error="handleImageError"
                class="screenshot-image"
              />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Información adicional -->
      <div v-if="result.screen" class="screen-info">
        <h4>📱 Información de la pantalla final</h4>
        <div class="info-grid">
          <div class="info-item">
            <strong>Título:</strong> {{ result.screen.title || 'N/A' }}
          </div>
          <div class="info-item">
            <strong>H1:</strong> {{ result.screen.h1 || 'N/A' }}
          </div>
          <div class="info-item">
            <strong>Usuario:</strong> {{ result.screen.visible_user || 'N/A' }}
          </div>
          <div class="info-item">
            <strong>Navegación:</strong> {{ result.screen.nav_items?.join(', ') || 'N/A' }}
          </div>
          <div class="info-item">
            <strong>CTAs:</strong> {{ result.screen.primary_ctas?.join(', ') || 'N/A' }}
          </div>
        </div>
      </div>
      
      <!-- Resultado de la tarea -->
      <div v-if="result.task_result && result.task_result.length > 0" class="task-result">
        <h4>🎯 Resultado de la tarea</h4>
        <ul>
          <li v-for="(item, index) in result.task_result" :key="index">{{ item }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
}

.form-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

h2 {
  color: #495057;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #495057;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
}

textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
  background-color: #007bff;
  color: white;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}



button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
}

.error h3 {
  color: #721c24;
  margin-top: 0;
}

.result {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
  border-radius: 4px;
  padding: 20px;
}

.result h3 {
  color: #0c5460;
  margin-top: 0;
  margin-bottom: 20px;
}

.test-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 25px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 6px;
}

.info-item {
  font-size: 14px;
}

.info-item strong {
  color: #495057;
}

.screenshots-section {
  margin-bottom: 25px;
}

.screenshots-section h4 {
  color: #495057;
  margin-bottom: 15px;
}

.screenshots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.screenshot-item {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.screenshot-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.screenshot-header {
  padding: 12px 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.step-number {
  display: block;
  font-weight: 600;
  color: #007bff;
  margin-bottom: 5px;
}

.url {
  display: block;
  font-size: 12px;
  color: #6c757d;
  word-break: break-all;
}

.screenshot-container {
  position: relative;
  overflow: hidden;
}

.screenshot-image {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
  min-height: 200px;
  background: #f8f9fa;
}

.image-error {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  background: #f8f9fa;
  color: #6c757d;
  font-style: italic;
  border: 2px dashed #dee2e6;
}

.screen-info {
  margin-bottom: 25px;
}

.screen-info h4 {
  color: #495057;
  margin-bottom: 15px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 6px;
}

.task-result {
  margin-bottom: 20px;
}

.task-result h4 {
  color: #495057;
  margin-bottom: 15px;
}

.task-result ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-result li {
  padding: 8px 12px;
  margin-bottom: 5px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 4px;
  border-left: 3px solid #28a745;
}

pre {
  background: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

@media (max-width: 768px) {
  .screenshots-grid {
    grid-template-columns: 1fr;
  }
  
  .test-info,
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
