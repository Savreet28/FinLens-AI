// On Vercel, VITE_API_URL is set to the Render backend URL; locally we use the dev server
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

// Shared helper: send a request, return the JSON, or throw a readable error
async function request(path, options) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, options)
  } catch {
    throw new Error('Could not reach the server. Is the backend running?')
  }

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    if (typeof data.detail === 'string') throw new Error(data.detail)
    if (Array.isArray(data.detail)) throw new Error(data.detail[0].msg) // 422 validation errors
    throw new Error('Something went wrong. Please try again.')
  }

  return data
}

export function uploadDocument(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request('/api/documents/upload', { method: 'POST', body: formData })
}

export function researchQuestion(question) {
  return request('/api/research', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
}

export function getDocuments() {
  return request('/api/documents')
}