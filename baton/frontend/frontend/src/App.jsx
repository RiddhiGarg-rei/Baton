import { useCallback, useEffect, useState } from "react";
import * as api from "./api";
import ProjectBar from "./components/ProjectBar";
import UploadForm from "./components/UploadForm";
import SourceList from "./components/SourceList";
import ChunkViewer from "./components/ChunkViewer";

const STORAGE_KEY = "baton.projectId";

export default function App() {
  const [project, setProject] = useState(null);
  const [sources, setSources] = useState([]);
  const [selectedSource, setSelectedSource] = useState(null);
  const [error, setError] = useState("");

  const refreshSources = useCallback(async (projectId) => {
    setSources(await api.listSources(projectId));
  }, []);

  // Reopen the last project after a page refresh.
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return;
    api
      .getProject(saved)
      .then(async (p) => {
        setProject(p);
        await refreshSources(p.id);
      })
      .catch(() => localStorage.removeItem(STORAGE_KEY));
  }, [refreshSources]);

  async function handleCreate(name) {
    setError("");
    try {
      const p = await api.createProject(name);
      localStorage.setItem(STORAGE_KEY, String(p.id));
      setProject(p);
      setSources([]);
      setSelectedSource(null);
    } catch (e) {
      setError(e.message);
    }
  }

  function handleSwitch() {
    localStorage.removeItem(STORAGE_KEY);
    setProject(null);
    setSources([]);
    setSelectedSource(null);
    setError("");
  }

  // UploadForm shows upload errors itself, so this lets them pass through.
  async function handleUpload(file, level) {
    const created = await api.uploadSource(project.id, file, level);
    await refreshSources(project.id);
    setSelectedSource(created);
    return created;
  }

  return (
    <div className="mx-auto max-w-5xl px-5 py-6">
      <header className="mb-6">
        <h1 className="font-serif text-4xl font-bold">Baton</h1>
        <p className="text-muted">Handovers where every claim shows its source.</p>
      </header>

      <main className="space-y-5">
        <ProjectBar project={project} onCreate={handleCreate} onSwitch={handleSwitch} />

        {error && (
          <p role="alert" className="rounded-lg bg-rose-100 p-3 text-sm text-rose-900">
            {error}
          </p>
        )}

        {project && (
          <div className="grid gap-5 md:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
            <div className="space-y-5">
              <UploadForm onUpload={handleUpload} />
              <SourceList
                sources={sources}
                selectedId={selectedSource?.id}
                onSelect={setSelectedSource}
              />
            </div>
            <ChunkViewer source={selectedSource} />
          </div>
        )}
      </main>
    </div>
  );
}
