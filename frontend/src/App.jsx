import { useState } from 'react'
import UploadPanel from './components/UploadPanel'
import QuestionForm from './components/QuestionForm'
import AnswerCard from './components/AnswerCard'
import EvidenceList from './components/EvidenceList'
import { uploadDocument, researchQuestion } from './api'
import MetricsChart from './components/MetricsChart'

function App() {
  // --- Documents ---
  const [documents, setDocuments] = useState([])

  // Change one document's fields (e.g. its status) by name
  function updateDocument(name, changes) {
    setDocuments((prev) =>
      prev.map((doc) => (doc.name === name ? { ...doc, ...changes } : doc))
    )
  }

  // Upload each selected file to FastAPI, one at a time
  async function handleFilesSelected(selectedFiles) {
    for (const file of selectedFiles) {
      setDocuments((prev) => [
        ...prev.filter((doc) => doc.name !== file.name),
        { name: file.name, status: 'uploading' },
      ])

      try {
        const data = await uploadDocument(file)
        updateDocument(file.name, {
          status: 'done',
          pages: data.pages_with_text,
          chunks: data.chunks,
        })
      } catch (error) {
        updateDocument(file.name, { status: 'error', message: error.message })
      }
    }
  }

  // --- Research ---
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleResearch() {
    setIsLoading(true)
    setError('')
    setResult(null)

    try {
      const data = await researchQuestion(question)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold text-slate-900">FinLens-AI</h1>
          <p className="text-sm text-slate-600">
            AI Financial Research &amp; Evidence Assistant
          </p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        <UploadPanel documents={documents} onFilesSelected={handleFilesSelected} />

        <QuestionForm
          question={question}
          onQuestionChange={setQuestion}
          onSubmit={handleResearch}
          isLoading={isLoading}
        />

        {error && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {error}
          </div>
        )}

        {result && (
          <>
          <AnswerCard answer={result.answer} found={result.found} />
            {result.sources.length > 0 && <EvidenceList sources={result.sources} />}
            
            {result.metrics && <MetricsChart metrics={result.metrics} />}
          </>
        )}
      </main>
    </div>
  )
}

export default App