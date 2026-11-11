import AccessChip from "./AccessChip";

export default function SourceList({ sources, selectedId, onSelect }) {
  return (
    <section className="rounded-xl border border-line bg-white p-4">
      <h2 className="mb-3 font-serif text-xl font-bold">Sources</h2>
      {sources.length === 0 ? (
        <p className="text-muted">No sources yet. Upload a file to get started.</p>
      ) : (
        <ul className="space-y-2">
          {sources.map((s) => (
            <li key={s.id}>
              <button
                type="button"
                onClick={() => onSelect(s)}
                aria-pressed={s.id === selectedId}
                className={`w-full rounded-lg border p-3 text-left hover:bg-page ${
                  s.id === selectedId ? "border-accent bg-page" : "border-line"
                }`}
              >
                <span className="block font-bold">{s.filename}</span>
                <span className="mt-1 flex flex-wrap items-center gap-2 text-sm text-muted">
                  <AccessChip level={s.access_level} />
                  <span>{s.chunk_count} chunk(s)</span>
                  {s.redactions > 0 && <span>{s.redactions} redacted</span>}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
