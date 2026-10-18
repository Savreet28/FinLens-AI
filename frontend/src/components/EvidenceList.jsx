function EvidenceList({ sources }) {
  return (
    <section className="bg-white rounded-xl border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900">Evidence</h2>

      <div className="mt-4 space-y-4">
        {sources.map((source, index) => (
          <div key={index} className="border-l-4 border-slate-300 pl-4">
            <p className="text-sm font-medium text-slate-900">
              {source.document}
              <span className="ml-2 text-slate-500 font-normal">
                Page {source.page}
              </span>
              {source.distance !== undefined && (
                <span className="ml-2 text-xs text-slate-400 font-normal">
                  match {(1 - source.distance).toFixed(2)}
                </span>
              )}
            </p>
            <p className="mt-1 text-sm text-slate-600 italic">
              "{source.text}"
            </p>
          </div>
        ))}
      </div>
    </section>
  )
}

export default EvidenceList