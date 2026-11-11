# Demo data (synthetic)

A fully fictional project used to test Baton: **Orbit Tech Club**, a student club running a workshop series.
Every name, email, phone number, token and amount here is invented. No real people or confidential material.

## What is in it

| Folder / file | Access level | Purpose |
|---|---|---|
| `project-repo/README.md` | public | Partly out-of-date README |
| `project-repo/docs/deploy.md` | team | Deployment notes |
| `project-repo/issues-export.md` | team | Issue tracker export |
| `notes/` (two meeting notes) | team | Decisions and open questions |
| `chat/core-team-chat.txt` | team | Chat export with the real story and some mistakes |
| `board/tasks.csv` | team | Task board export |
| `lead-only/sponsor-agreement-summary.md` | lead_only | Sponsor terms and amount |
| `restricted/finance-ledger.csv` | restricted | Club finances |
| `manifest.json` | | Access levels, upload names and role clearances |
| `ANSWER-KEY.md` | | What a correct run should find (do not upload) |
| `load_demo.py` | | Uploads everything to a running backend |

## Planted tests

The data deliberately contains conflicting statements, missing reasons, an unowned deadline, a task marked
done that is not, restricted material, and fake secrets for redaction. See `ANSWER-KEY.md` for the full list
with line numbers.

## Load it

With the backend running:

```bash
python load_demo.py --dry-run   # preview
python load_demo.py             # upload all files with their access levels
```

Or upload files by hand in the backend's `/docs` page, using the access level shown in `manifest.json`.
