// Generic questions that work for any company's financial report
const EXAMPLE_QUESTIONS = [
  'What was the total revenue, and how did it change?',
  'What drove the change in net income?',
  'What are the main risks to the business?',
  'How much cash does the company have?',
]

function QuestionForm({ question, onQuestionChange, onSubmit, isLoading, hasDocuments }) {
  function handleSubmit(event) {
    event.preventDefault()
    onSubmit()
  }

  const canSubmit = hasDocuments && question.trim().length >= 3 && !isLoading

  return (
    <section className="bg-white rounded-xl border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900">Ask a Financial Question</h2>

      <form onSubmit={handleSubmit} className="mt-4 flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          placeholder="e.g. Why did revenue increase this year?"
          disabled={isLoading}
          className="flex-1 rounded-lg border border-slate-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-400 disabled:bg-slate-50"
        />
        <button
          type="submit"
          disabled={!canSubmit}
          className="rounded-lg bg-slate-900 px-6 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Researching...' : 'Research'}
        </button>
      </form>

      {!hasDocuments && (
        <p className="mt-3 text-sm text-amber-700">
          Upload at least one document before asking a question.
        </p>
      )}

      <div className="mt-4 flex flex-wrap gap-2">
        {EXAMPLE_QUESTIONS.map((example) => (
          <button
            key={example}
            type="button"
            onClick={() => onQuestionChange(example)}
            disabled={isLoading}
            className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs text-slate-600 hover:bg-slate-100 disabled:opacity-40"
          >
            {example}
          </button>
        ))}
      </div>
    </section>
  )
}

export default QuestionForm