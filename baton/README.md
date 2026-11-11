# Baton

**An evidence-linked, permission-aware knowledge-handover platform.**

Baton turns a team's scattered project activity (repositories, notes, tasks and chats) into a handover the incoming person can trust. Every claim links back to its source, uncertainty is shown instead of hidden, a human approves everything before it is shared, and each person sees only what they are cleared to see.

Built for the three-round hackathon challenge *"Prevent Critical Knowledge From Leaving With People"*.

> **Project status: Round 1 (The Plan).**
> The problem analysis, workflow, architecture and development plan are complete and documented in [`docs/PLAN.md`](docs/PLAN.md).
> Application code is **not** in this repository yet. It will be added, with a visible commit history, during the official build window.

Project page: see the `docs/` folder (published with GitHub Pages).

---

## The problem

When someone leaves a project, the documents stay but the understanding walks out. The incoming person cannot tell what was decided, why, what is half-finished, who owns what, or who to ask. Generic AI summaries make it worse: they sound confident, invent missing links and ignore who is allowed to see what.

## The solution

1. **Connect** authorised sources (GitHub repository, documents, notes, task-board export, chat export), each tagged with an access level. Sensitive patterns are redacted on the way in.
2. **Reconstruct** the project state as structured claims: decisions, owners, risks, dependencies, open questions, next actions, plus a timeline.
3. **Verify** each claim against its cited evidence and label it *Supported*, *Inferred*, *Conflicting* or *Missing evidence*.
4. **Review**: the outgoing member answers targeted gap questions; a reviewer edits, rejects and approves. Every change is versioned.
5. **Handover**: the incoming person gets a role-based view built only from evidence they may access, a first-week plan, and an Acknowledge button.

**What makes it different:** gap-driven exit questions. Baton detects what it cannot know and asks the outgoing person specific questions. Their answers are stored as *Self-reported* sources, kept distinct from machine-verified evidence.

## Trust principles

- No claim without evidence.
- Uncertainty is shown, never hidden.
- Permissions are applied *before* generation, so restricted information cannot leak into a summary.
- The AI only proposes; a human decides.

## Planned tech stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite, Tailwind CSS |
| Backend | Python + FastAPI |
| Database / search | SQLite (SQLAlchemy), FTS5, sentence-transformers |
| AI | Hosted LLM API (structured JSON output) plus a verification pass |
| Integrations | GitHub REST API, file parsers (pypdf, python-docx, markdown, csv) |
| Auth / access | JWT, role-based access control, per-source ACL tags |
| Deployment | Vercel (frontend), Render (backend) |

## Repository layout

```
baton/
  docs/          Project page (GitHub Pages) and the Round 1 plan
  backend/       FastAPI service (to be built in the build window)
  frontend/      React app (to be built in the build window)
  demo-data/     Synthetic demo project (to be created in the build window)
```

## Roadmap

| Round | Goal |
|---|---|
| 1. The Plan | Understand the problem, design the workflow and architecture (done) |
| 2. The Build | Working end-to-end MVP with evidence-linked claims, review and one role-based view |
| 3. The Finish | Exit questions, permission-aware Q&A, version history and audit log, testing and polish |

## Data and privacy

Only synthetic, public or permissioned data will ever be used for demonstrations. Do not upload confidential material without permission.

## Disclosure

AI assistance is used for planning, writing and code support. Significant AI tools, libraries and templates will be listed here and in the Round 2 document as they are added.

## Author

Riddhi Garg, B.Tech CSE, VIT Vellore. Team: Code crusader (solo entry).

## License

[MIT](LICENSE)
