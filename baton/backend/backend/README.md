# Baton backend

FastAPI service. Current scope (steps 1 to 4):

1. Health check
2. Upload a `.txt`, `.md` or `.csv` file, redact sensitive details, split into chunks with line numbers
3. Store projects, sources and chunks in SQLite
4. Fetch any chunk together with its citation (for example `notes.md, lines 14-18`)

Not built yet: LLM claim extraction, verification, roles and permission filtering, review workflow.
Access levels are stored on every source but **not enforced yet**, so do not use real confidential data.

## Run it

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs. In that page you can:

1. `POST /projects` with `{"name": "Tech Club"}`
2. `POST /projects/1/sources`, choose `samples/notes-2026-03-12.md`, set an access level
3. `GET /sources/1/chunks` and notice the redacted email, phone, and secrets
4. `GET /chunks/1` to see the text with its citation

## Test it

```bash
pytest
```

## Layout

```
app/chunking.py    split text into chunks that keep their line numbers
app/redaction.py   hide emails, phone numbers and secrets before storing
app/db.py          SQLite tables and queries
app/main.py        the API routes
tests/             automated tests
samples/           synthetic sample file for trying the upload
```
