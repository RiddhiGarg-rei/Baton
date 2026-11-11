# Baton

Baton helps a team hand a project over to the next person. It ingests a team's notes, chat and task exports, redacts sensitive details, and splits everything into chunks that each cite their source file and line range.

## Try it

**Live app:** https://riddhigarg-rei.github.io/Baton/

The backend runs on a free server that sleeps when idle, so **the first load can take up to a minute**. If something fails right away, wait a minute and try again.

1. Click **Create project** and give it a name.
2. Upload a sample file from [`baton/demo-data/demo-data/`](baton/demo-data/demo-data/), for example `notes/2026-03-12-sync.md` or `chat/core-team-chat.txt`.
3. Pick an access level for the file.
4. Open the source and click a chunk to see its text and citation (file and line range).

Please use only the synthetic sample files. Do not upload real or confidential data.

## What works

- Create a project
- Upload `.txt`, `.md` and `.csv` files (up to 1 MB) with an access level
- Redact sensitive details before storage, with counts shown
- Split sources into chunks that keep their line numbers
- Open any chunk with a source-and-line citation

## What does not work yet

- Claim extraction, verification and status labels
- Exit questions, review and approval, role-based handover views, Q&A
- Access levels are saved but not enforced; there is no login or roles
- PDF and DOCX uploads and the GitHub connector

## Tech stack

- **Frontend:** React 18, Vite, Tailwind CSS (GitHub Pages)
- **Backend:** Python, FastAPI, SQLite (Render)
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