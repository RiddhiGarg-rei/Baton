# Known limitations and roadmap

## Limitations today

- **No LLM yet.** The system stores, redacts, chunks and cites, but does not extract claims.
- **No login or roles.** Access levels are stored but not enforced, so use synthetic data only.
- **Redaction is pattern-based.** It catches common formats and will miss others.
- **Text files only.** `.txt`, `.md` and `.csv`, up to 1 MB. CSV files are treated as plain text.
- **Single-file database.** SQLite is fine for a demo, not for many simultaneous users.
- **No deployment hardening.** No rate limiting, HTTPS setup or encryption at rest.
- **English-centred.** Patterns and demo data assume English text and Indian phone formats.

## Roadmap

| Stage | Goal |
|---|---|
| Next | LLM claim extraction as structured JSON, each claim linked to chunk citations |
| Next | Verification pass and the four status labels (Supported, Inferred, Conflicting, Missing evidence) |
| Round 2 target | Review and approve screen, one role-based view, basic role enforcement, deployed link |
| Round 3 target | Exit questions, permission-aware Q&A, version history and audit log, hardening |
| After the event | More connectors (GitHub, Slack, Drive, Notion), single sign-on, continuous mode, self-hosted model option, bus-factor analytics |

See `PROGRESS.md` for the live feature table.
