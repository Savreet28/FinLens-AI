function LoadingCard() {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6" aria-live="polite">
      <div className="flex items-center gap-3">
        <div className="h-5 w-5 animate-spin rounded-full border-2 border-slate-300 border-t-slate-900" />
        <p className="text-sm font-medium text-slate-700">
          Searching your documents and writing a grounded answer...
        </p>
      </div>

      <div className="mt-5 space-y-3 animate-pulse">
        <div className="h-3 w-full rounded bg-slate-200" />
        <div className="h-3 w-5/6 rounded bg-slate-200" />
        <div className="h-3 w-2/3 rounded bg-slate-200" />
      </div>
    </section>
  )
}

export default LoadingCard
