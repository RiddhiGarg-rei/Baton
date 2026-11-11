import { useEffect, useState } from "react";
import * as api from "../api";
import { citationLabel } from "../citation";
import AccessChip from "./AccessChip";

export default function ChunkViewer({ source }) {
  const [chunks, setChunks] = useState([]);
  const [detail, setDetail] = useState(null); // the chunk plus its official citation
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Load the chunks whenever a different source is chosen.
  useEffect(() => {
    if (!source) return;
    let cancelled = false;
    setLoading(true);
    setError("");
    setDetail(null);
    api
      .listChunks(source.id)
      .then((data) => !cancelled && setChunks(data))
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [source]);

  async function openChunk(chunk) {
    setError("");
    try {
      setDetail(await api.getChunk(chunk.id));
    } catch (e) {
      setError(e.message);
    }
  }

  if (!source) {
    return (
      <section className="rounded-xl border border-line bg-white p-4">
        <h2 className="mb-2 font-serif text-xl font-bold">Evidence</h2>
        <p className="text-muted">Choose a source to see its chunks and citations.</p>
      </section>
    );
  }

  return (
    <section className="rounded-xl border border-line bg-white p-4">
      <h2 className="mb-1 font-serif text-xl font-bold">Evidence from {source.filename}</h2>
      <p className="mb-3 text-sm text-muted">
        Each chunk remembers exactly where it came from. Select one to see its citation.
      </p>

      {error && (
        <p role="alert" className="mb-3 rounded-lg bg-rose-100 p-3 text-sm text-rose-900">
          {error}
        </p>
      )}
      {loading && <p className="text-muted">Loading...</p>}

      <ul className="mb-4 space-y-2">
        {chunks.map((c) => (
          <li key={c.id}>
            <button
              type="button"
              onClick={() => openChunk(c)}
              aria-pressed={detail?.chunk_id === c.id}
              className={`w-full rounded-lg border p-3 text-left hover:bg-page ${
                detail?.chunk_id === c.id ? "border-accent bg-page" : "border-line"
              }`}
            >
              <code className="text-xs text-muted">
                {citationLabel(source.filename, c.start_line, c.end_line)}
              </code>
              <span className="mt-1 block text-sm">
                {c.text.length > 110 ? `${c.text.slice(0, 110)}...` : c.text}
              </span>
            </button>
          </li>
        ))}
      </ul>

      {detail && (
        <article className="rounded-lg border-2 border-accent p-4" aria-live="polite">
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <strong>Citation:</strong>
            <code className="rounded bg-page px-2 py-0.5 text-sm">{detail.citation.label}</code>
            <AccessChip level={detail.access_level} />
          </div>
          <pre className="whitespace-pre-wrap break-words font-sans text-sm leading-relaxed">
            {detail.text}
          </pre>
          <p className="mt-3 text-xs text-muted">
            Access levels are shown but not enforced yet. Use only synthetic data for now.
          </p>
        </article>
      )}
    </section>
  );
}
