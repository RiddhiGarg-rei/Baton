# Progress against the plan

> Last updated: [date]. Edit the **Status** column to match what you have actually run and seen working.
> Status words: **Working** (run and checked), **Built** (code written, not yet checked end to end),
> **Planned** (not started).

## Feature status

| Area | Feature | Status |
|---|---|---|
| Sources | Upload `.txt`, `.md`, `.csv` | Built |
| Sources | PDF and DOCX upload | Planned |
| Sources | GitHub repository connector | Planned |
| Privacy | Redaction before storage | Working (unit-tested) |
| Evidence | Line-aware chunking and citations | Working (unit-tested) |
| Evidence | Click-through citation in the UI | Built |
| Storage | Projects, sources, chunks in SQLite | Working (unit-tested) |
| Permissions | Access levels stored | Built |
| Permissions | Role-based filtering and enforcement | Planned |
| Reconstruction | LLM claim extraction and timeline | Planned |
| Verification | Status labels, conflict detection, missing evidence | Planned |
| Review | Edit, reject, approve; version history; audit log | Planned |
| Handover | Role-based views, first-week plan, acknowledgement | Planned |
| Uncertainty | Gap-driven exit questions with self-reported answers | Planned |
| Demo data | Synthetic project with answer key | Working |

## Changes from the Round 1 plan

| Plan said | What changed | Why |
|---|---|---|
| SQLAlchemy for the database | Built-in `sqlite3` for now | Simpler to learn and test first; see `DECISIONS.md` |
| GitHub connector in the first build | Deferred; file upload first | Reaches an end-to-end flow sooner |
| PDF and DOCX parsing early | Deferred | Text formats cover the demo data |

## Commitments for Round 3 (to be confirmed)

1. **Gap-driven exit questions** with self-reported evidence and re-verification after answers.
2. **Permission-aware "Ask the handover" Q&A** that answers only from cited, cleared evidence and says
   "I don't know" otherwise.
3. **Version history with diff, audit log and acknowledgement tracking**, with evidence-quality scoring and export.

## Evidence of work

- Commit history: see the repository.
- Demo data and answer key: `demo-data/`.
- Test notes: `TESTING.md`.
