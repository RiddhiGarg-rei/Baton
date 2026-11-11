# Testing

> Fill in the "Result" and "Date" cells yourself after running each item. Do not record a result you have not
> seen.

## Automated tests (`backend/tests/`)

Run from the `backend` folder:

```bash
pytest
```

| File | What it checks | Tests |
|---|---|---|
| `test_chunking.py` | Empty text, short text, exact line ranges, paragraph splits, oversized lines | 5 |
| `test_redaction.py` | Emails, phones, tokens and secrets removed; dates and line numbers untouched; line count unchanged | 4 |
| `test_db.py` | Store and read back a citation, label format, invalid access level rejected, cascade delete | 4 |
| `test_api.py` | Health, upload then redact then chunk then cite, bad uploads, 404s, blank project name | 5 |

| Run date | Command | Result |
|---|---|---|
| [date] | `pytest` | [for example: 18 passed] |

## Manual journeys with the demo data

Start the backend, run `python load_demo.py` in `demo-data/`, start the frontend, then check:

| # | Journey | Expected | Result |
|---|---|---|---|
| 1 | Create a project in the UI | Project name and id appear | [ ] |
| 2 | Upload `notes/2026-03-12-sync.md` as Team | Success message mentions 2 redactions | [ ] |
| 3 | Open its chunks | No email or phone number visible; `[REDACTED:...]` tags instead | [ ] |
| 4 | Upload `chat/core-team-chat.txt` | Token and `admin password` value are redacted | [ ] |
| 5 | Click a chunk | Citation like `core-team-chat.txt, lines 1-9` and the matching text | [ ] |
| 6 | Refresh the page | Same project reopens with its sources | [ ] |
| 7 | Stop the backend and click Upload | Clear error: cannot reach the backend | [ ] |

## Failure cases

| Case | Expected | Result |
|---|---|---|
| Upload a `.exe` or `.pdf` | 415 with a readable message | [ ] |
| Upload an empty file | 422 "File has no text" | [ ] |
| Upload a file over 1 MB | 413 | [ ] |
| Upload a non-UTF-8 file | 400 | [ ] |
| Create a project with a blank name | Rejected, no project created | [ ] |
| Request a chunk id that does not exist | 404 | [ ] |

## Checks that need later features

These are written in `demo-data/ANSWER-KEY.md` and will be run once claims and roles exist: expected claims and
statuses, gap questions, permission tests (Web Developer must not see the sponsorship amount or the ledger),
and redaction coverage.

## Structured tester feedback

| Tester (role) | Task given | What went wrong or was confusing | Change made |
|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] |
