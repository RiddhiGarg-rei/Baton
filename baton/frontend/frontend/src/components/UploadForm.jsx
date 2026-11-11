import { useRef, useState } from "react";
import { ACCESS_LEVELS } from "../citation";

export default function UploadForm({ onUpload }) {
  const fileRef = useRef(null);
  const [level, setLevel] = useState("team");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  async function submit(e) {
    e.preventDefault();
    const file = fileRef.current?.files?.[0];
    if (!file) {
      setError("Choose a .txt, .md or .csv file first.");
      return;
    }
    setBusy(true);
    setError("");
    setResult(null);
    try {
      const created = await onUpload(file, level);
      setResult(created);
      fileRef.current.value = "";
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="rounded-xl border border-line bg-white p-4">
      <h2 className="mb-3 font-serif text-xl font-bold">Add a source</h2>

      <label htmlFor="file" className="mb-1 block text-sm font-bold">
        File (.txt, .md or .csv, up to 1 MB)
      </label>
      <input
        id="file"
        ref={fileRef}
        type="file"
        accept=".txt,.md,.csv"
        className="mb-3 block w-full text-sm"
      />

      <label htmlFor="level" className="mb-1 block text-sm font-bold">
        Who may see it
      </label>
      <select
        id="level"
        value={level}
        onChange={(e) => setLevel(e.target.value)}
        className="mb-3 w-full rounded-lg border border-line bg-white px-3 py-2"
      >
        {ACCESS_LEVELS.map((a) => (
          <option key={a.value} value={a.value}>
            {a.label}
          </option>
        ))}
      </select>

      <button
        type="submit"
        disabled={busy}
        className="rounded-lg bg-accent px-4 py-2 font-bold text-white hover:brightness-110 disabled:opacity-60"
      >
        {busy ? "Uploading..." : "Upload"}
      </button>

      {error && (
        <p role="alert" className="mt-3 rounded-lg bg-rose-100 p-3 text-sm text-rose-900">
          {error}
        </p>
      )}
      {result && (
        <p role="status" className="mt-3 rounded-lg bg-emerald-100 p-3 text-sm text-emerald-900">
          Stored {result.filename} as {result.chunk_count} chunk(s).{" "}
          {result.redactions > 0
            ? `${result.redactions} sensitive item(s) were redacted before saving.`
            : "No sensitive items were found."}
        </p>
      )}
    </form>
  );
}
