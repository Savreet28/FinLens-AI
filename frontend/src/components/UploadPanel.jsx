function UploadPanel({ files, onFilesChange }) {
  function handleChange(event) {
    const selected = Array.from(event.target.files)
    onFilesChange(selected)
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

      {files.length > 0 && (
        <ul className="mt-4 space-y-1">
          {files.map((file) => (
            <li key={file.name} className="text-sm text-slate-700">
              ✓ {file.name}
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

export default UploadPanel