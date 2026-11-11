// All calls to the Baton backend live here, so the rest of the app never builds URLs by hand.
const BASE = "/api"; // Vite forwards this to http://127.0.0.1:8000 (see vite.config.js)

async function request(path, options = {}) {
  let res;
  try {
    res = await fetch(`${BASE}${path}`, options);
  } catch {
    throw new Error("Cannot reach the backend. Is it running at http://127.0.0.1:8000 ?");
  }

  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") message = body.detail;
      else if (Array.isArray(body.detail)) message = body.detail.map((d) => d.msg).join("; ");
    } catch {
      // The error body was not JSON; keep the default message.
    }
    throw new Error(message);
  }
  return res.json();
}

export const createProject = (name) =>
  request("/projects", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });

export const getProject = (id) => request(`/projects/${id}`);

export const listSources = (projectId) => request(`/projects/${projectId}/sources`);

export function uploadSource(projectId, file, accessLevel) {
  const form = new FormData();
  form.append("file", file);
  form.append("access_level", accessLevel);
  return request(`/projects/${projectId}/sources`, { method: "POST", body: form });
}

export const listChunks = (sourceId) => request(`/sources/${sourceId}/chunks`);

export const getChunk = (chunkId) => request(`/chunks/${chunkId}`);
