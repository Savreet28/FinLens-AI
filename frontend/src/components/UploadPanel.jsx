function UploadPanel({ documents, onFilesSelected }) {
  function handleChange(event) {
    const selected = Array.from(event.target.files)
    onFilesSelected(selected)
    event.target.value = '' // lets you pick the same file again later
  }

  return (
    <section className="bg-white rounded-xl border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900">
        Upload Financial Documents
      </h2>
      <p className="text-sm text-slate-500 mt-1">PDF files only</p>

      <input
        type="file"
        accept=".pdf"
        multiple
        onChange={handleChange}
        className="mt-4 block w-full text-sm text-slate-600 file:mr-4 file:rounded-lg file:border-0 file:bg-slate-900 file:px-4 file:py-2 file:text-white hover:file:bg-slate-700"
      />

      {documents.length > 0 && (
        <ul className="mt-4 space-y-2">
          {documents.map((doc) => (
            <li key={doc.name} className="text-sm">
              {doc.status === 'uploading' && (
                <span className="text-slate-500">⏳ {doc.name} — extracting, chunking & embedding...</span>
              )}
              {doc.status === 'done' && (
                <span className="text-green-700">
                  ✓ {doc.name} — {doc.pages} pages, {doc.chunks} chunks indexed
                </span>
              )}
              {doc.status === 'error' && (
                <span className="text-red-600">✗ {doc.name} — {doc.message}</span>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

export default UploadPanel