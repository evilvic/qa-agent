import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

export const post = (url, data) => {
  return api.post(url, data)
}

export const postQA = async (instructions, headful = false, maxSteps = 16) => {
  try {
    const response = await api.post('/run', {
      instructions,
      headful,
      max_steps: maxSteps
    })
    return response.data
  } catch (error) {
    console.error('Error en postQA:', error)
    throw error
  }
}

// Función para obtener la URL de las imágenes locales
export const getImageUrl = (localPath) => {
  // Extraer el run_id del path local
  const runIdMatch = localPath.match(/artifacts\/([^\/]+)/)
  if (runIdMatch) {
    const runId = runIdMatch[1]
    const fileName = localPath.split('/').pop()
    // Construir URL directa al servidor backend
    return `http://127.0.0.1:8000/artifacts/${runId}/screens/${fileName}`
  }
  return localPath
}

export default api