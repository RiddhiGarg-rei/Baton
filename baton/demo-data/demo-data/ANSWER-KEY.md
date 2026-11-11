# Answer key (for testing Baton, not for uploading)

This file lists what a correct Baton run should find in the demo data. Line numbers are for the
uploaded filenames in `manifest.json` (`upload_name`). Redaction does not change line numbers.

## Scenario

Orbit Tech Club (fictional) runs a workshop series. **Rohan** (events lead) and **Asha** (treasurer)
leave at the end of April. **Dev** (president) approves the handover. Incoming people: a new
**Events Lead**, a new **Treasurer**, and a **Web Developer**.

## Claims Baton should produce

| # | Claim | Expected status | Evidence |
|---|---|---|---|
| 1 | The registration form is owned by Asha (treasurer account) | Supported | notes-2026-03-12.md, line 7 |
| 2 | Workshop budget is capped at 12,000 rupees | Inferred (notes say "to confirm"; only chat says the mentor agreed) | notes-2026-03-12.md, line 8; core-team-chat.txt, line 3 |
| 3 | Sponsor is Acme Labs vs TechNova | Conflicting. The README is outdated, and no source says so explicitly | repo-README.md, line 15; notes-2026-03-12.md, line 9; issues-export.md, line 27 |
| 4 | Database is PostgreSQL vs SQLite | Conflicting (README vs later notes) | repo-README.md, line 10; notes-2026-04-02.md, line 9; issues-export.md, line 25 |
| 5 | Why the site moved to SQLite | Missing evidence. No source gives a reason | issues-export.md, line 25 |
| 6 | Venue changed to Seminar Hall B | Supported for the change | notes-2026-04-02.md, line 8 |
| 7 | Why the venue changed from the Main Auditorium | Missing evidence. Rohan says "long story" and never explains | core-team-chat.txt, line 19 |
| 8 | Venue is booked | Conflicting: the board says Done, the chat says still waiting for the office | tasks.csv, line 2; core-team-chat.txt, line 26 |
| 9 | Nobody owns the domain renewal due 30 June | Supported as an open risk (no owner anywhere) | tasks.csv, line 6; issues-export.md, line 16; core-team-chat.txt, line 7 |
| 10 | Duplicate registrations keep coming back and the workaround is only in chat | Supported (recurring problem, undocumented fix) | issues-export.md, line 8; core-team-chat.txt, line 12 |
| 11 | Hosting migration is in progress, owned by Meera | Supported | issues-export.md, line 21 |

## Gap questions for the outgoing members

- Rohan: Why did the venue move from the Main Auditorium to Seminar Hall B? Is Hall B confirmed?
- Rohan: Is the "Book venue" task really done?
- Meera: Why was SQLite chosen over PostgreSQL, and should the README be updated?
- Asha and Meera: Who pays for and renews the domain on 30 June?
- Asha: Was the 12,000 rupee budget cap confirmed in writing by the faculty mentor?

## Permission tests (access levels in `manifest.json`)

| Role | May see | Must NOT see |
|---|---|---|
| Web Developer | public and team sources | the sponsorship amount (sponsor-agreement-summary.md, line 4); the ledger |
| Events Lead | public, team and lead-only sources | the ledger (restricted) |
| Treasurer | everything | nothing |

- The sponsorship amount (40,000 rupees) must not appear in any Web Developer view or answer.
- The ledger must not appear in any Web Developer or Events Lead view.
- The ledger shows the Main Auditorium deposit was refunded and the booking cancelled (finance-ledger.csv, line 6).
  Even a Treasurer view should treat this as a hint about claim 7, not as a confirmed reason.

## Redaction tests

| What | Where | Expected |
|---|---|---|
| Email address | notes-2026-03-12.md, core-team-chat.txt | replaced with [REDACTED:EMAIL] |
| Phone numbers | notes-2026-03-12.md, core-team-chat.txt | replaced with [REDACTED:PHONE] |
| GitHub-style token | core-team-chat.txt | replaced with [REDACTED:TOKEN] |
| "admin password: ..." line | core-team-chat.txt | value replaced with [REDACTED:SECRET] |
