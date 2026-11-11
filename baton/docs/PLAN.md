# Baton: Round 1 plan (summary)

## 1. The problem
Documents stay when someone leaves, but the reasoning behind decisions, unfinished work, dependencies, recurring problems and contacts disappear. Existing handover documents are written once, from memory, with no link between a claim and its evidence. Generic AI summaries read confidently, invent missing links and ignore access rules.

**Scope:** turn authorised project activity into a reviewed, evidence-linked, role-appropriate handover, and mark honestly what is still unknown. Baton is not a general knowledge base, chat product or project-management tool.

## 2. Users
| User | Need |
|---|---|
| Incoming member (primary) | Ownership, risks, blockers and next actions, with a source for each claim, and nothing they are not cleared to see |
| Outgoing member | Hand over without writing a long document; targeted questions instead of a blank page |
| Reviewer / approver | Correct, reject and approve before sharing; version history and acknowledgements |
| Project admin | Control over connected sources and access rules |

Scenarios: annual club leadership change, mid-semester exit from a project team, research group turnover, temporary absence.
Primary setting: student technical clubs and project teams (generalises to workplaces, research groups and volunteer communities).

## 3. Solution
Ingest authorised sources, reconstruct the project as structured, evidence-backed claims, let a human review and approve them, then publish a different handover view for each incoming role.

Design principles: no claim without evidence; uncertainty is a feature; permission before generation; human in control.

Distinctive idea: **gap-driven exit questions** whose answers are stored as *Self-reported* sources.

## 4. Workflow
Connect, Reconstruct, Verify, Review, Handover (see README). Failure handling: if a source cannot be parsed or evidence is thin, Baton says so instead of filling the gap. Rejected claims are not re-introduced unless new evidence appears.

## 5. Planned features
Upload and GitHub ingestion; claim extraction and timeline; citations with a click-through source viewer; conflict detection and missing-evidence flags; gap-driven exit questions; edit / reject / approve with version history and audit log; source-level access tags with pre-generation filtering and redaction; role-based views with first-week plan and acknowledgement; permission-aware "Ask the handover" Q&A; evidence-quality score and export; synthetic demo data.

## 6. Architecture
Sources -> Ingestion (parse, chunk, tag ACL, redact) -> Reconstruction (LLM extraction) -> Verification (evidence check, conflicts, gaps) -> Evidence store -> Review workspace -> Permission filter -> Role views.

Each claim stores: type, text, status, confidence, evidence[] (source ID, location, quoted span), access level (strictest of its evidence), reviewer decision, version.

## 7. Development plan
- **Round 1:** plan, research, wireframes, architecture and evidence model.
- **Round 2:** working MVP, deployed link, repository, updated architecture document, testing notes.
- **Round 3:** exit questions, permission-aware Q&A, version history with diff and audit log, hardening, accessibility and security pass, demo video and report.

## 8. Expected impact (targets, not proven results)
Faster transition for the incoming person; every key claim opens a valid source; zero restricted items visible to lower-clearance roles in the permission tests; gaps turned into answered questions before departure; each handover has an approver, history and acknowledgement.

## 9. Future scope
Slack, Discord, Teams, Drive, Notion, Jira and Trello connectors; single sign-on; continuous mode; self-hosted or on-device model option; role templates; bus-factor analytics; mobile app and reminders.
