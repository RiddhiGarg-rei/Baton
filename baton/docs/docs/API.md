# Backend API

Base URL during development: `http://127.0.0.1:8000`. Interactive docs: `http://127.0.0.1:8000/docs`.

**No authentication or access enforcement yet.** `access_level` is stored and returned, but it does not
restrict who can read a chunk. Use synthetic data only.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Check the service is running |
| POST | `/projects` | Create a project |
| GET | `/projects/{project_id}` | Read a project |
| POST | `/projects/{project_id}/sources` | Upload a file (redacted, chunked, stored) |
| GET | `/projects/{project_id}/sources` | List a project's sources |
| GET | `/sources/{source_id}/chunks` | List a source's chunks |
| GET | `/chunks/{chunk_id}` | Read one chunk with its citation |

## Examples

### Create a project

```
POST /projects
{"name": "Orbit Workshop Series 2026"}
```
Response `201`:
```json
{"id": 1, "name": "Orbit Workshop Series 2026", "created_at": "2026-04-10 09:30:00"}
```

### Upload a source

`POST /projects/1/sources` as `multipart/form-data` with fields `file` and `access_level`
(`public`, `team`, `lead_only` or `restricted`; default `team`).

Response `201`:
```json
{
  "id": 1, "project_id": 1, "filename": "notes-2026-03-12.md", "kind": "markdown",
  "access_level": "team", "redactions": 2, "created_at": "2026-04-10 09:31:00",
  "chunk_count": 2, "redaction_counts": {"email": 1, "phone": 1}
}
```

Limits: `.txt`, `.md` or `.csv` only, UTF-8 text, up to 1 MB.

### Read a chunk with its citation

`GET /chunks/3`
```json
{
  "chunk_id": 3,
  "text": "- Keep the registration form in the club workspace. ...",
  "access_level": "team",
  "citation": {
    "source_id": 1, "filename": "notes-2026-03-12.md",
    "start_line": 5, "end_line": 12,
    "label": "notes-2026-03-12.md, lines 5\u201312"
  }
}
```

## Errors

| Status | When |
|---|---|
| 400 | Uploaded file is not UTF-8 text |
| 404 | Project, source or chunk does not exist |
| 413 | File is larger than 1 MB |
| 415 | File type is not `.txt`, `.md` or `.csv` |
| 422 | Empty file, blank project name, or invalid access level |

Error bodies look like `{"detail": "File is larger than 1 MB"}`.

## Planned endpoints

Claim extraction, claim review and approval, role-based handover views, exit questions, acknowledgement and
version history. These will be added in later rounds.
