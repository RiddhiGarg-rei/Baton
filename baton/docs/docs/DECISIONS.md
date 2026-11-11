# Technical decisions

Each entry says what was decided, why, and what it costs.

## 1. Redact before storing

**Decision:** Sensitive patterns (emails, phone numbers, tokens, `password: ...` style values) are replaced
before a source is saved.
**Why:** If raw secrets never reach the database, they cannot leak from it later, from logs, or into a future
LLM prompt.
**Cost:** Redaction is pattern-based and will miss unusual formats. It is a safety net, not a guarantee. The
original uploaded file is not kept.

## 2. Chunks keep line ranges

**Decision:** Text is split on line boundaries and each chunk stores its start and end line.
**Why:** Citations must point to an exact place a person can check. Cutting lines in half would break that.
**Cost:** A very long single line becomes one large chunk. Redaction never changes the number of lines, so line
numbers stay valid.

## 3. Python's built-in `sqlite3` instead of SQLAlchemy

**Decision:** The backend uses `sqlite3` directly, with plain SQL in one file.
**Why:** Fewer moving parts to learn first, and the data layer can be tested with no extra installs. This
**changes the Round 1 plan**, which named SQLAlchemy.
**Cost:** More hand-written SQL. Moving to SQLAlchemy or PostgreSQL later is straightforward because all queries
live in `db.py`.

## 4. Store access levels now, enforce them later

**Decision:** Every source has an access level from the first upload, but no role checks exist yet.
**Why:** The data model must carry access levels from the start so enforcement can be added without migrating
data. Each future claim will inherit the strictest level of its evidence.
**Cost:** Until enforcement is built, the API must not be used with real confidential data. This is stated in
the API docs and in the interface.

## 5. Each request gets its own database connection

**Decision:** A connection is opened per request and always closed (`get_conn` in `main.py`).
**Why:** Avoids sharing one connection between threads, and keeps tests isolated.
**Cost:** Slight overhead per request, which is fine at this scale.

## 6. Strict upload rules

**Decision:** Only `.txt`, `.md` and `.csv`, UTF-8, up to 1 MB. Folder parts of a filename are dropped.
**Why:** Small attack surface, predictable parsing, and enough for notes, chat exports and board exports.
**Cost:** PDF and DOCX support is deferred.

## 7. Vite proxy for development

**Decision:** The frontend calls `/api/...` and Vite forwards to port 8000.
**Why:** No cross-origin (CORS) configuration needed in development.
**Cost:** A deployed version will need either the same proxy idea or explicit CORS settings.

## 8. The LLM proposes, a person decides (planned)

**Decision:** Generated claims must cite evidence and pass a verification step, and nothing is shared until a
person approves it.
**Why:** The challenge forbids presenting assumptions as verified organisational truth.
