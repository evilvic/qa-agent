# main.py
import os, json, shutil, uuid, asyncio, time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv

from browser_use import Agent, ChatOpenAI, Browser

# Cargar .env robusto
load_dotenv(find_dotenv(usecwd=True), override=True)

# ---------- Config ----------
ARTIFACTS_ROOT = Path(os.getenv("ARTIFACTS_DIR", "artifacts")).resolve()
ARTIFACTS_ROOT.mkdir(parents=True, exist_ok=True)
SEMAPHORE = asyncio.Semaphore(int(os.getenv("MAX_CONCURRENCY", "1")))

# ---------- Models ----------
class RunRequest(BaseModel):
    instructions: str = Field(..., description="Objetivo a ejecutar DESPUÉS del login")
    headful: bool = Field(False, description="Si true, abre navegador visible")
    max_steps: int = Field(16, ge=1, le=60, description="Pasos máximos del agente")

class ScreenDescription(BaseModel):
    url: str
    title: str
    h1: str | None = None
    nav_items: list[str] = []
    primary_ctas: list[str] = []
    visible_user: str | None = None

class RunResponse(BaseModel):
    run_id: str
    artifacts_dir: str
    screen: ScreenDescription
    task_result: dict | list | None
    urls: list[str]
    screenshots: list[str]
    video_dir: str
    traces_dir: str
    har_path: str
    elapsed_ms: int

# ---------- Helpers ----------
def _allowed_domains(url: str) -> list[str]:
    host = (urlparse(url).hostname or "").lower()
    return [host, f"*.{host}"] if host else []

IPHONE_VIEWPORT = {"width": 390, "height": 844}  # iPhone-ish

def _make_task(base_url: str, email: str, password: str, login_hint: str, user_instructions: str) -> str:
    target_url = base_url.rstrip("/") + login_hint if login_hint else base_url
    return f"""
AGENTE DE QA — CONTRATO GENERAL (MÓVIL / ANTI-LOOP / FLEXIBLE)

OBJETIVO:
{user_instructions}

ENTORNO:
- App minu en viewport móvil (pantalla estrecha).
- URL inicial: {target_url}

REGLAS GENERALES (OBLIGATORIAS):
1) Idempotencia de navegación:
   - Antes de hacer clic para navegar, verifica si YA estás en el destino.
   - Comprueba estado con cualquiera de:
     • La URL contiene el destino esperado (p. ej., /inside/xxxx)
     • El ítem de menú correspondiente está activo (aria-current/activo)
     • El encabezado principal (h1/h2) o contenido esperado es visible
   - Si ya estás ahí, NO vuelvas a hacer clic.

2) Presupuesto y límites:
   - Máximo 6 clics de navegación por ejecución.
   - Máximo 1 clic por misma etiqueta/menú (no repetir "X" dos veces).
   - Si un clic no produce el estado esperado, prueba UNA alternativa (otro selector/link sinónimo) y sigue. No reintentes más.

3) Overlays/Tours/Modales:
   - Si aparece un tour/overlay (p. ej., botones "Continuar/Comenzar/Confirmar"), ciérralo o acéptalo UNA sola vez y continúa.
   - No vuelvas a abrirlo.

4) Anti ping-pong:
   - Si detectas alternancia entre dos estados/URLs (A↔B), NO repitas. Ajusta tu plan para cumplir el objetivo sin rebotar.

5) "Volver/Regresar":
   - Si el objetivo implica regresar, hazlo UNA sola vez al lugar inmediatamente anterior y TERMINA.
   - No vuelvas a navegar después de completar el regreso.

LOGIN (si no estás autenticado):
1) Abre {target_url}
2) Pulsa "Iniciar sesión".
3) Completa:
   - Email/Teléfono: "{email}"
   - Contraseña: "{password}"
4) Envía con "Iniciar sesión" y espera señales de sesión (dashboard, avatar/nombre, botón "Cerrar sesión", navegación interna).

EJECUCIÓN POST-LOGIN:
- Ejecuta el OBJETIVO siguiendo las REGLAS GENERALES.
- Tras cada acción, valida éxito (URL/encabezado/ítem activo/contenido). 
- Si el estado no cambia, no repitas ciegamente: usa UNA alternativa y sigue.
- Si el OBJETIVO implica listar/extraer elementos (beneficios, KPIs, ítems, etc.):
  • Navega a la sección correcta.
  • Haz scroll razonable para ver elementos cargados.
  • Expande "Ver más/Ver detalle" UNA vez si existe.
  • Devuelve un JSON **natural para el objetivo**:
    - Si es una lista, usa una lista de objetos con campos autoexplicativos (p. ej., name, short_desc, value, cta_label, etc.).
    - Si es un único dato, devuelve un objeto con claves claras.
  • No dupliques elementos; máximo 20.

CRITERIO DE FINALIZACIÓN (STOP):
- Termina en cuanto el OBJETIVO quede cumplido.
- Si el OBJETIVO incluye varios sub-pasos (p. ej., "ir a X y luego regresar"), marca cada sub-paso como completado UNA sola vez. Al completar el último, TERMINA.

FORMATO DE ENTREGA — EXACTAMENTE DOS BLOQUES JSON EN ESTE ORDEN:
1) SCREEN JSON (primero), ajustado al esquema:
{{
  "url": "<url actual>",
  "title": "<título o ''>",
  "h1": "<primer H1 visible o null>",
  "nav_items": ["<hasta 6 ítems de navegación>"],
  "primary_ctas": ["<hasta 3 CTAs principales>"],
  "visible_user": "<nombre/email visible o null>"
}}
2) RESULT JSON (segundo y ÚLTIMO contenido del mensaje):
- Debe ser un **objeto o una lista** que represente el resultado del OBJETIVO (flexible según el caso).
- Nada de texto fuera de esos dos JSON.

NOTAS:
- No muestres la contraseña.
- Si no hay H1 válido, usa null (no cadenas como "$0").
- No repitas navegación.
"""

def _extract_last_json_block(text: str):
    """Toma el último bloque JSON (objeto o lista) del texto; si falla, devuelve None."""
    if not text:
        return None
    # intenta lista
    li, ri = text.rfind("["), text.rfind("]")
    if li != -1 and ri != -1 and ri > li:
        frag = text[li:ri+1]
        try:
            return json.loads(frag)
        except Exception:
            pass
    # intenta objeto
    li, ri = text.rfind("{"), text.rfind("}")
    if li != -1 and ri != -1 and ri > li:
        frag = text[li:ri+1]
        try:
            return json.loads(frag)
        except Exception:
            pass
    return None

# ---------- App ----------
app = FastAPI(title="Minu QA AI", version="0.4.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos de artifacts
app.mount("/artifacts", StaticFiles(directory=str(ARTIFACTS_ROOT)), name="artifacts")

@app.get("/healthz")
def healthz():
    keys = ["TEST_BASE_URL","TEST_LOGIN_PATH","TEST_USER_EMAIL","OPENAI_API_KEY","ARTIFACTS_DIR","LLM_MODEL"]
    return {k: bool(os.getenv(k)) for k in keys}

@app.post("/run", response_model=RunResponse)
async def run(req: RunRequest):
    base_url = os.getenv("TEST_BASE_URL")
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    login_hint = (os.getenv("TEST_LOGIN_PATH") or "").strip()
    llm_model = os.getenv("LLM_MODEL", "gpt-4.1-mini")

    if not (base_url and email and password and os.getenv("OPENAI_API_KEY")):
        raise HTTPException(status_code=500, detail="Faltan variables necesarias (base_url/email/password o OPENAI_API_KEY)")

    run_id = f"{datetime.now():%Y%m%d_%H%M%S}_{uuid.uuid4().hex[:8]}"
    run_dir = ARTIFACTS_ROOT / run_id
    screens_dir = run_dir / "screens"
    video_dir = run_dir / "video"
    traces_dir = run_dir / "traces"
    for d in (screens_dir, video_dir, traces_dir):
        d.mkdir(parents=True, exist_ok=True)

    task = _make_task(base_url, email, password, login_hint, req.instructions)
    allowed = _allowed_domains(base_url)

    start = time.perf_counter()

    async with SEMAPHORE:
        browser = Browser(
            headless=not req.headful,
            allowed_domains=allowed,
            window_size=IPHONE_VIEWPORT,          # 👈 iPhone-like
            record_video_dir=str(video_dir),
            record_har_path=str(run_dir / "trace.har"),
            traces_dir=str(traces_dir),
        )
        llm = ChatOpenAI(model=llm_model)

        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            output_model_schema=ScreenDescription,  # valida el primer bloque (screen)
            max_steps=req.max_steps,
        )
        history = await agent.run()

    # Copiar screenshots
    screenshots_abs: list[str] = []
    for src in history.screenshot_paths():
        try:
            dst = screens_dir / Path(src).name
            shutil.copy2(src, dst)
            screenshots_abs.append(str(dst))
        except FileNotFoundError:
            pass

    # 1) SCREEN
    screen: ScreenDescription = history.structured_output
    if screen.h1 is not None and screen.h1.strip() in {"", "$0"}:
        screen.h1 = None
    (run_dir / "screen.json").write_text(json.dumps(screen.model_dump(), indent=2, ensure_ascii=False))

    # 2) RESULT (flexible)
    final_text = history.final_result() or ""
    task_result = _extract_last_json_block(final_text)
    (run_dir / "result.json").write_text(json.dumps(task_result, indent=2, ensure_ascii=False))

    elapsed_ms = int((time.perf_counter() - start) * 1000)

    return RunResponse(
        run_id=run_id,
        artifacts_dir=str(run_dir),
        screen=screen,
        task_result=task_result,
        urls=history.urls(),
        screenshots=screenshots_abs,
        video_dir=str(video_dir),
        traces_dir=str(traces_dir),
        har_path=str(run_dir / "trace.har"),
        elapsed_ms=elapsed_ms,
    )
