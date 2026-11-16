// True only on the live site (set VITE_DEMO_MODE=true in Vercel)
// (accepts "true", "TRUE", " true " etc.)
const DEMO_MODE =
  String(import.meta.env.VITE_DEMO_MODE ?? '').trim().toLowerCase() === 'true';

function UploadPanel({ documents, onFilesSelected }) {
  function handleChange(event) {
    const selected = Array.from(event.target.files);
    onFilesSelected(selected);
    event.target.value = ''; // lets you pick the same file again later
  }

  return (
    <section className="bg-white rounded-xl border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900">
        Upload Financial Documents
      </h2>

      {DEMO_MODE ? (
        <p className="mt-3 rounded-lg bg-blue-50 border border-blue-200 p-3 text-sm text-blue-800">
          Live demo: a public sample report (NVIDIA 10-Q) is already loaded, so
          you can ask questions right away. Uploads are turned off here. Clone
          the GitHub repo to use your own documents.
        </p>
      ) : (
        <>
          <p className="text-sm text-slate-500 mt-1">
            PDF files only
          </p>

          <input
            type="file"
            accept=".pdf"
            multiple
            onChange={handleChange}
            className="mt-4 block w-full text-sm text-slate-600 file:mr-4 file:rounded-lg file:border-0 file:bg-slate-900 file:px-4 file:py-2 file:text-white hover:file:bg-slate-700"
          />
        </>
      )}

      {documents.length === 0 && (
        <p className="mt-4 text-sm text-slate-400">
          No documents indexed yet. Upload a PDF to get started.
        </p>
      )}

      {documents.length > 0 && (
        <>
          <h3 className="mt-5 text-sm font-semibold text-slate-700">
            Indexed documents
          </h3>

          <ul className="mt-2 space-y-2">
            {documents.map((doc) => (
              <li key={doc.name} className="text-sm">
                {doc.status === 'uploading' && (
                  <span className="text-slate-500">
                    ⏳ {doc.name} — extracting, chunking & embedding...
                  </span>
                )}

                {doc.status === 'done' && (
                  <span className="text-green-700">
                    ✓ {doc.name} —{' '}
                    {doc.pages ? `${doc.pages} pages, ` : ''}
                    {doc.chunks} chunks indexed
                  </span>
                )}

                {doc.status === 'error' && (
                  <span className="text-red-600">
                    ✗ {doc.name} — {doc.message}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}

export default UploadPanel;