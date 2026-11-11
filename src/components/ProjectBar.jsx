import { useState } from "react";

export default function ProjectBar({ project, onCreate, onSwitch }) {
  const [name, setName] = useState("");

  if (project) {
    return (
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-line bg-white p-4">
        <p>
          <span className="text-muted">Project: </span>
          <strong>{project.name}</strong>
          <span className="text-muted"> (#{project.id})</span>
        </p>
        <button
          type="button"
          onClick={onSwitch}
          className="rounded-lg border-2 border-line px-3 py-1.5 text-sm font-bold hover:bg-page"
        >
          Start a new project
        </button>
      </div>
    );
  }

  function submit(e) {
    e.preventDefault();
    if (!name.trim()) return;
    onCreate(name.trim());
    setName("");
  }

  return (
    <form
      onSubmit={submit}
      className="flex flex-wrap items-end gap-3 rounded-xl border border-line bg-white p-4"
    >
      <div className="grow">
        <label htmlFor="project-name" className="mb-1 block text-sm font-bold">
          Project name
        </label>
        <input
          id="project-name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          maxLength={100}
          placeholder="Orbit Workshop Series 2026"
          className="w-full rounded-lg border border-line px-3 py-2"
        />
      </div>
      <button
        type="submit"
        className="rounded-lg bg-accent px-4 py-2 font-bold text-white hover:brightness-110"
      >
        Create project
      </button>
    </form>
  );
}
