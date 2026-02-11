# QA Agent

Agente de QA automatizado para la app **minu**. Usa un navegador controlado por LLM ([browser_use](https://github.com/browser-use/browser-use) + OpenAI) para hacer login, navegar la app y devolver descripciones estructuradas de pantalla junto con resultados de tareas.

## Estructura

```
backend/    → API en FastAPI + agente browser_use
frontend/   → UI en Vue 3 + Vite (bun)
```

## Setup

### Variables de entorno

Crea `backend/.env`:

```env
TEST_BASE_URL=https://pwa.minu.mx
TEST_LOGIN_PATH=/login
TEST_USER_EMAIL=tu@email.com
TEST_USER_PASSWORD=tu_password
OPENAI_API_KEY=sk-...
```

Opcionales: `ARTIFACTS_DIR` (default: `artifacts`), `LLM_MODEL` (default: `gpt-4.1-mini`), `MAX_CONCURRENCY` (default: `1`).

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
bun install
bun run dev
```

El frontend corre en `http://localhost:5173` y se conecta al backend en `http://localhost:8000`.

## Uso

1. Levanta el backend (`uvicorn main:app --reload`)
2. Levanta el frontend (`bun run dev`)
3. Escribe instrucciones de QA en la UI (ej: "Navega a beneficios y lista los disponibles")
4. El agente ejecuta las instrucciones en un navegador, captura screenshots/video/traces y devuelve resultados estructurados

## Tests

```bash
cd backend
pytest                                           # todos los tests
pytest tests/test_smoke.py::test_home_smoke -v   # un test específico
```
