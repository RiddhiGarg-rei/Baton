# Baton

Baton helps a team hand a project over to the next person. It ingests a team's notes, chat and task exports, redacts sensitive details, and splits everything into chunks that each cite their source file and line range.

## Try it

**Live app:** https://riddhigarg-rei.github.io/Baton/

The backend runs on a free server that sleeps when idle, so **the first load can take up to a minute**. If something fails right away, wait a minute and try again.

1. Open the live app and click **Load demo project**. This creates a synthetic student-club project and uploads nine sample sources (meeting notes, team chat, a task board, repo docs, and two restricted files).
2. Click any source in the list to see its chunks.
3. Click a chunk to read its text and its citation (source file and line range).
4. Check the sources that contain emails or phone numbers to see how many sensitive details were redacted.

You can also click **Create project** to start empty and upload your own `.txt`, `.md` or `.csv` files. Sample files are in [`baton/demo-data/demo-data/`](baton/demo-data/demo-data/). Please use only synthetic data, not real or confidential files.

## What works

- Create a project, or load the ready-made demo project
- Upload `.txt`, `.md` and `.csv` files (up to 1 MB) with an access level
- Redact sensitive details before storage, with counts shown
- Split sources into chunks that keep their line numbers
- Open any chunk with a source-and-line citation

## What does not work yet

- Claim extraction, verification and status labels
- Exit questions, review and approval, role-based handover views, Q&A
- Access levels are saved but not enforced; there is no login or roles, so every visitor can see every chunk
- PDF and DOCX uploads and the GitHub connector
- The free server resets when it restarts, so projects can disappear

## Tech stack

- **Frontend:** React 18, Vite, Tailwind CSS (hosted on GitHub Pages)
- **Backend:** Python, FastAPI, SQLite (hosted on Render)
- **AI:** none. Redaction and chunking are rule-based.

## Run locally

Backend:

```bash
cd baton/backend/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (from the repo root, in a second terminal):

```bash
npm install
npm run dev
```

Backend tests: run `pytest` inside `baton/backend/backend`.

## Disclosure

AI assistance was used for code and writing support. Libraries are listed in `package.json` and `baton/backend/backend/requirements.txt`.