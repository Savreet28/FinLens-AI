function AnswerCard({ answer }) {
  return (
    <section className="bg-white rounded-xl border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900">AI Research Answer</h2>
      <p className="mt-3 text-slate-700 leading-relaxed whitespace-pre-line">
        {answer}
      </p>
    </section>
  )
}
export default AnswerCard