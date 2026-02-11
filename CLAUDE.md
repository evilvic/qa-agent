# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered QA automation agent for the **minu** web app. An LLM-driven browser agent (via `browser_use` + OpenAI) performs login, navigates the app, and returns structured screen descriptions plus task results. A Vue 3 frontend provides a UI for submitting test instructions and viewing results.

## Repository Structure

```
backend/              # Python backend — FastAPI + browser_use agent
  main.py             # API server: /healthz, POST /run
  tests/              # pytest async tests (browser_use integration)
frontend/             # Vue 3 frontend — Vite SPA
  src/
    App.vue           # Main component (form + results display)
    api.js            # Axios client hitting localhost:8000
```

## Commands

### Backend (backend/)

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

### Frontend (frontend/)

```bash
cd frontend && bun install
cd frontend && bun run dev      # Vite dev server on localhost:5173
cd frontend && bun run build    # Production build
```

## Environment Variables

The backend reads from `.env` (via `python-dotenv`). Required:

| Variable | Purpose |
|---|---|
| `TEST_BASE_URL` | Target app URL (e.g., `https://pwa.minu.mx`) |
| `TEST_USER_EMAIL` | Login email |
| `TEST_USER_PASSWORD` | Login password |
| `OPENAI_API_KEY` | OpenAI API key for the LLM agent |

Optional: `TEST_LOGIN_PATH` (login route, e.g. `/login`), `ARTIFACTS_DIR` (default: `artifacts`), `LLM_MODEL` (default: `gpt-4.1-mini`), `MAX_CONCURRENCY` (default: `1`).

## Architecture Notes

- **POST /run** is the core endpoint. It builds a detailed Spanish-language task prompt (`_make_task`), launches a `browser_use.Agent` with an iPhone-sized viewport (390x844), and collects screenshots, video, HAR, and Playwright traces into a timestamped `artifacts/<run_id>/` directory.
- The agent returns two JSON blocks: a `ScreenDescription` (validated via Pydantic `output_model_schema`) and a flexible task result (extracted by `_extract_last_json_block`).
- Concurrency is controlled by an `asyncio.Semaphore`.
- The frontend talks to `http://127.0.0.1:8000` and resolves screenshot URLs through `/artifacts/` static file serving.
- Tests are async (`pytest.ini` sets `asyncio_mode = auto`) and use the same `browser_use` agent directly.
- All agent task prompts are written in Spanish and include anti-loop, idempotent navigation, and budget rules.
