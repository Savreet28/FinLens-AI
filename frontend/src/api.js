const API_BASE_URL = 'http://127.0.0.1:8000'

export async function uploadDocument(file) {
  // Pack the file the same way an HTML form would
  const formData = new FormData()
  formData.append('file', file)

  let response
  try {
    response = await fetch(`${API_BASE_URL}/api/documents/upload`, {
      method: 'POST',
      body: formData,
    })
  } catch {
    // fetch only throws when the server can't be reached at all
    throw new Error('Could not reach the server. Is the backend running?')
  }

  // Read the JSON body (fall back to {} if the body isn't JSON)
  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    const message = typeof data.detail === 'string' ? data.detail : 'Upload failed.'
    throw new Error(message)
  }

  return data
}