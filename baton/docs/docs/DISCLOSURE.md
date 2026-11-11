# Disclosure

## Contribution

Solo entry. One participant is responsible for product, design, backend, frontend, data and documentation.

## AI assistance

An AI assistant (Claude, by Anthropic) was used to help plan the project, draft documentation, and draft code
and test files. The participant is responsible for reviewing, running and understanding everything that is
submitted. No AI model is called by the current application code.

## Libraries and services

| Name | Used for | Licence type |
|---|---|---|
| FastAPI | Backend web framework | MIT |
| Uvicorn | Running the backend | BSD |
| python-multipart | File uploads | Apache-2.0 |
| Pydantic (installed with FastAPI) | Request validation | MIT |
| pytest | Automated tests | MIT |
| httpx | API tests and demo loader | BSD |
| SQLite (Python `sqlite3`) | Database | Public domain |
| React and React DOM | Frontend | MIT |
| Vite and `@vitejs/plugin-react` | Frontend build and dev server | MIT |
| Tailwind CSS, PostCSS, Autoprefixer | Styling | MIT |
| Google Fonts (Atkinson Hyperlegible, Newsreader) | Page typography, loaded from Google | Open Font License |
| GitHub and GitHub Pages | Code hosting and the project page | n/a |

Check each project's own page for the exact licence terms.

## APIs and AI models

| Item | Status |
|---|---|
| LLM API (Claude or Gemini) for claim extraction | Planned, not used yet |
| GitHub REST API connector | Planned, not used yet |
| Embedding model (sentence-transformers) | Planned, not used yet |

When added, keys will live only in environment variables and will never be committed.

## Data

Only synthetic data is used. See `demo-data/README.md`. No real people, organisations' confidential
material, or personal data.

## Templates and boilerplate

No project template was used. Configuration files follow each tool's standard documentation. Previously written
code: none.
