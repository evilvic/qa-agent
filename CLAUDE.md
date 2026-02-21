# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Product Vision

AI-powered QA automation platform. An LLM-driven browser agent executes test cases against any web app, evaluates pass/fail with evidence, and accumulates memory across executions to optimize cost and speed. See `docs/CONTEXT.md` for full product context.

**This is an app-agnostic product.** No references to specific target apps in code, prompts, or docs.

## Documentation System

| File | Purpose |
|------|---------|
| `docs/PLAN.md` | Master execution plan — phases, domain model, success criteria |
| `docs/CONTEXT.md` | Product context — vision, competitor analysis, principles |
| `docs/DECISIONS.md` | Decision log — every decision with trade-offs and status |
| `docs/PROGRESS.md` | Chronological progress — what was done, when, blockers |
| `docs/phases/PHASE-N.md` | Phase detail — tasks, criteria, deliverables |

**Rules:**
- Every architectural decision goes in DECISIONS.md before implementation
- Every session's work gets logged in PROGRESS.md
- Phase files are the source of truth for what to build and in what order
- CLAUDE.md stays focused on technical guidance, not product vision

## Commands

### Backend (from repo root)

```bash
# Setup (one time)
cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# Start the API server
cd backend && source .venv/bin/activate && uvicorn main:app --reload

# Run all tests
cd backend && source .venv/bin/activate && pytest

# Run a single test
cd backend && source .venv/bin/activate && pytest tests/test_smoke.py::test_home_smoke -v
```

Tests require Playwright browsers installed (`playwright install chromium`) and valid credentials in `backend/.env`. They are async (`pytest.ini` sets `asyncio_mode = auto`) and launch real browser sessions against the target app.

### Frontend (from repo root)

```bash
cd frontend && bun install
cd frontend && bun run dev      # Vite dev server on localhost:5173
cd frontend && bun run build    # Production build
```

## Environment Variables

The backend reads from `backend/.env` (via `python-dotenv`). Copy `backend/.env.example` to get started.

**Required:** `TEST_BASE_URL`, `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`, `OPENAI_API_KEY`

**Optional:**
- `TEST_LOGIN_PATH` — login route (default: none)
- `ARTIFACTS_DIR` — artifacts storage path (default: `artifacts`)
- `LLM_MODEL` — default model (default: `gpt-4.1-mini`)
- `MAX_CONCURRENCY` — concurrent runs (default: `1`)
- `CHROME_PATH` — custom Chrome/Chromium binary path
- `AGENT_TIMEOUT` — max seconds per agent run (default: `120`)

## Architecture

### Current state (PoC)

- **Backend:** FastAPI with single `POST /run` endpoint. Uses `browser_use.Agent` + `ChatOpenAI`.
- **Frontend:** Vue 3 SPA (Vite + bun). Single `App.vue` component.
- **No persistence.** Results only exist in memory during the session.

### Target state (MVP — Fase 1)

- **Backend:** FastAPI with CRUD endpoints for Projects, Test Cases, Runs. SQLite via SQLModel.
- **Frontend:** Vue 3 with Vue Router. Views for projects, test cases, run history, run detail.
- **Persistence:** SQLite database at `backend/data/qa_agent.db`.
- **Pass/fail:** LLM evaluates test result against expected outcome.

See `docs/PLAN.md` for full architecture evolution and `docs/phases/PHASE-1.md` for current phase detail.

### Key patterns

- Agent prompts are in **Spanish**. All user-facing text is in Spanish.
- `browser_use.Agent` is the core dependency for browser automation.
- Artifacts (screenshots, video, HAR, traces) are saved to `artifacts/<run_id>/`.
- Concurrency controlled by `asyncio.Semaphore`.
- Prompt builder lives in `backend/prompt.py` (to be extracted from `main.py`).

## Code Conventions

- **Language:** Python 3.12+ (backend), JavaScript/Vue 3 (frontend)
- **API style:** RESTful, snake_case in Python, camelCase in JavaScript
- **Models:** Pydantic for validation, SQLModel for persistence
- **Async:** All agent operations are async
- **Error handling:** Never return generic 500s. Always structured error responses.
- **Logging:** Structured JSON logging via Python `logging` module
