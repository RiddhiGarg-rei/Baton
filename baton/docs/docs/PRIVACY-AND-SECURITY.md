# Privacy, security and accessibility

## Data used

Only synthetic data is used (`demo-data/`). Every name, email, phone number, token and amount in it is invented.
Do not upload confidential material without permission.

## What is protected today

| Protection | How it works | Limits |
|---|---|---|
| Redaction before storage | Emails, phone numbers, common token formats and `password/secret/token/api_key = value` are replaced with tags like `[REDACTED:EMAIL]` | Pattern-based; unusual formats are missed |
| Upload validation | File type, size (1 MB) and UTF-8 checks; folder parts of filenames are removed | Content is not scanned for malware |
| Secrets out of the repo | `.gitignore` excludes `.env`, keys and databases; `.env.example` has no secrets | Relies on the developer not committing them |
| Safe database writes | Parameterised SQL everywhere; source and chunks saved in one transaction | n/a |

## What is NOT protected yet

- **No login and no roles.** Anyone who can reach the API can read every chunk.
- **Access levels are stored but not enforced.**
- No audit log, rate limiting or encryption at rest.

These are planned for later rounds, and the API must not be exposed publicly with real data until they exist.

## Planned controls

1. Role-to-clearance mapping (see `demo-data/manifest.json`): Web Developer sees public and team, Events Lead
   adds lead-only, Treasurer sees everything.
2. Filter evidence by clearance **before** any summary or answer is generated, so restricted text cannot leak.
3. A claim's access level is the strictest level among its evidence.
4. Audit log of who viewed, edited, approved and acknowledged each handover version.
5. LLM keys kept in environment variables, never in the repository.

## Using an external AI service (planned)

Text sent to a hosted LLM leaves this system. Some free tiers may use submitted content to improve their
products, so only synthetic or permissioned data may be sent. A self-hosted model option is on the roadmap.

## Accessibility (frontend)

Built in: labelled form fields, visible keyboard focus, buttons instead of clickable text, `role="alert"` on
errors, access levels shown as words as well as colour, and a layout that works on narrow screens.

Not yet checked: screen-reader testing, colour-contrast audit of every state, keyboard-only walkthrough of the
final review screens. These are planned for Round 3.
