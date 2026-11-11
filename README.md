# Baton frontend

React + Vite + Tailwind CSS. Current scope matches backend steps 1 to 4:

- Create a project
- Upload a `.txt`, `.md` or `.csv` file with an access level
- See the sources, how many chunks each has, and how many items were redacted
- Open any chunk to see its text and citation (for example `notes.md, lines 14-18`)

Not built yet: claims with status labels, the review and approval screens, role-based handover views, and access enforcement.

## Run it

You need Node.js 18 or newer, and the backend running first.

```bash
# terminal 1: backend
cd backend
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uvicorn app.main:app --reload

# terminal 2: frontend
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## How it talks to the backend

The app calls `/api/...` and Vite forwards those requests to `http://127.0.0.1:8000` (see `vite.config.js`),
so no extra backend settings are needed during development.

## Layout

```
src/api.js                 every backend call in one place
src/citation.js            citation label format and access levels
src/App.jsx                page state: project, sources, selected source
src/components/
  ProjectBar.jsx           create or switch project
  UploadForm.jsx           choose file and access level
  SourceList.jsx           uploaded sources
  ChunkViewer.jsx          chunks, plus the citation for the chosen chunk
  AccessChip.jsx           access level label
```

## Troubleshooting

- "Cannot reach the backend": start the backend first and check it answers at http://127.0.0.1:8000/health.
- Blank page: open the browser console (F12) and read the first red error.
