import { useState } from 'react'

const PREVIEW_LENGTH = 300 // characters shown before "Show more"


// One evidence card (used only inside this file)
// One evidence card (used only inside this file)
function EvidenceCard({ source }) {
  const [expanded, setExpanded] = useState(false)

  const isLong = source.text.length > PREVIEW_LENGTH
  const shownText =
    expanded || !isLong ? source.text : source.text.slice(0, PREVIEW_LENGTH) + '…'

  return (
    <div
      id={`source-${source.number}`}
      className={`scroll-mt-6 rounded-lg border p-4 ${
        source.cited ? 'border-blue-200 bg-blue-50' : 'border-slate-200 opacity-70'
      }`}
    >
      <div className="flex flex-wrap items-center gap-2 text-sm">
        <span className="rounded bg-blue-100 px-1.5 text-xs font-semibold text-blue-700">
          {source.number}
        </span>
        <span className="font-medium text-slate-900 break-all">{source.document}</span>
        <span className="text-slate-500">Page {source.page}</span>
        <span className="text-xs text-slate-400">
          match {(1 - source.distance).toFixed(2)}
        </span>
      </div>

      <p className="mt-2 text-sm text-slate-600 italic break-words">"{shownText}"</p>

      {isLong && (
        <button
          type="button"
          onClick={() => setExpanded(!expanded)}
          className="mt-1 text-xs font-medium text-blue-700 hover:underline"
        >
          {expanded ? 'Show less' : 'Show more'}
        </button>
      )}
    </div>
  )
}

function EvidenceList({ sources }) {
  const cited = sources.filter((source) => source.cited)
  const others = sources.filter((source) => !source.cited)

  return (
    <section className="bg-white rounded-xl border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900">Evidence</h2>
      <p className="mt-1 text-sm text-slate-500">
        Passages from your documents. Numbers match the citations in the answer.
      </p>

      {cited.length > 0 && (
        <div className="mt-4 space-y-3">
          <h3 className="text-sm font-semibold text-slate-700">Used in the answer</h3>
          {cited.map((source) => (
            <EvidenceCard key={source.number} source={source} />
          ))}
        </div>
      )}

      {others.length > 0 && (
        <div className="mt-6 space-y-3">
          <h3 className="text-sm font-semibold text-slate-500">Also retrieved (not cited)</h3>
          {others.map((source) => (
            <EvidenceCard key={source.number} source={source} />
          ))}
        </div>
      )}
    </section>
  )
}

export default EvidenceList