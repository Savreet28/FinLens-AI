function QuestionForm({ question, onQuestionChange, onSubmit }) {
  function handleSubmit(event) {
    event.preventDefault()
    onSubmit()
  }

  return (
    <section className="bg-white rounded-xl border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900">
        Ask a Financial Question
      </h2>

      <form onSubmit={handleSubmit} className="mt-4 flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          placeholder="e.g. Why did revenue increase this year?"
          className="flex-1 rounded-lg border border-slate-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-400"
        />
        <button
          type="submit"
          disabled={!question.trim()}
          className="rounded-lg bg-slate-900 px-6 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          Research
        </button>
      </form>
    </section>
  )
}

export default QuestionForm