function AnswerCard({ answer, found }) {
  // Split the text so citation markers like "[2]" become separate pieces:
  // "Revenue rose [1] due to demand [3]." → ["Revenue rose ", "[1]", " due to demand ", "[3]", "."]
  const parts = answer.split(/(\[\d+\])/)

  return (
    <section
      className={`rounded-xl border p-6 ${
        found ? 'bg-white border-slate-200' : 'bg-amber-50 border-amber-200'
      }`}
    >
      <h2 className="text-lg font-semibold text-slate-900">
        {found ? 'AI Research Answer' : 'No Answer Found in Your Documents'}
      </h2>

      <p className="mt-3 text-slate-700 leading-relaxed whitespace-pre-line">
        {parts.map((part, index) => {
          const match = part.match(/^\[(\d+)\]$/)
          if (!match) return <span key={index}>{part}</span>

          const number = match[1]
          return (
            <a
              key={index}
              href={`#source-${number}`}
              className="mx-0.5 inline-block rounded bg-blue-100 px-1.5 text-xs font-semibold text-blue-700 align-text-top hover:bg-blue-200"
            >
              {number}
            </a>
          )
        })}
      </p>
    </section>
  )
}

export default AnswerCard