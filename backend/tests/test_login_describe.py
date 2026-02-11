# tests/test_login_describe.py
import os, json, shutil
import pytest
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from browser_use import Agent, ChatOpenAI, Browser

load_dotenv()

class ScreenDescription(BaseModel):
    url: str = Field(description="URL actual tras el login")
    title: str = Field(description="Título de la pestaña/documento")
    h1: str | None = Field(default=None, description="Primer H1 visible o null")
    nav_items: list[str] = Field(default_factory=list, description="Hasta 6 items de navegación visibles")
    primary_ctas: list[str] = Field(default_factory=list, description="Hasta 3 botones/CTAs principales")
    visible_user: str | None = Field(default=None, description="Nombre/email visible del usuario logueado, si aparece")

def _allowed_domains_from(url: str) -> list[str]:
    host = (urlparse(url).hostname or "").strip().lower()
    return [d for d in [host, f"*.{host}"] if d]

# Permite configurar la carpeta raíz de artefactos vía env; por defecto: ./artifacts
ARTIFACTS_ROOT = Path(os.getenv("ARTIFACTS_DIR", "artifacts")).resolve()

@pytest.mark.asyncio
async def test_login_describe(request):
    base_url = os.environ.get("TEST_BASE_URL")
    user_email = os.environ.get("TEST_USER_EMAIL")
    user_password = os.environ.get("TEST_USER_PASSWORD")

    assert base_url and user_email and user_password, (
        "Faltan TEST_BASE_URL / TEST_USER_EMAIL / TEST_USER_PASSWORD en .env"
    )

    # Carpeta por corrida: artifacts/<timestamp>_<testname>/
    test_name = request.node.name.replace(os.sep, "_")
    run_dir = ARTIFACTS_ROOT / f"{datetime.now():%Y-%m-%d_%H-%M-%S}_{test_name}"
    screens_dir = run_dir / "screens"
    video_dir = run_dir / "video"
    traces_dir = run_dir / "traces"
    for d in (screens_dir, video_dir, traces_dir):
        d.mkdir(parents=True, exist_ok=True)

    login_hint = (os.environ.get("TEST_LOGIN_PATH") or "").strip()
    target_url = base_url.rstrip("/") + login_hint if login_hint else base_url

    browser = Browser(
        headless=True,
        allowed_domains=_allowed_domains_from(base_url),
        window_size={"width": 1280, "height": 800},
        record_video_dir=str(video_dir),              # ▶️ video persistente en artifacts
        record_har_path=str(run_dir / "trace.har"),   # 🌐 HAR persistente
        traces_dir=str(traces_dir),                   # 🧵 traces persistentes
    )

    task = f"""
Eres un agente de QA. Harás login en minu y luego describirás la pantalla autenticada.

1) Abre {target_url}
2) En la portada, haz clic en el botón que dice exactamente "Iniciar sesión".
3) En el formulario de login identifica los campos:
   - Email/teléfono: placeholder "Correo o Número de Celular"
   - Contraseña: placeholder "Contraseña"
   Escribe el email "{user_email}" y la contraseña "{user_password}".
4) Haz clic en el botón "Iniciar sesión".
5) Espera a que la sesión quede iniciada (dashboard, avatar/nombre, botón "Cerrar sesión").
6) Devuelve EXCLUSIVAMENTE un JSON:
{{
  "url": "<url actual>",
  "title": "<título de la pestaña>",
  "h1": "<primer H1 visible o null>",
  "nav_items": ["<hasta 6 items de navegación visibles>"],
  "primary_ctas": ["<hasta 3 CTAs principales>"],
  "visible_user": "<nombre/email visible del usuario o null>"
}}
No muestres la contraseña ni texto fuera del JSON.
"""

    agent = Agent(
        task=task,
        llm=ChatOpenAI(model="gpt-4.1-mini"),
        browser=browser,
        output_model_schema=ScreenDescription,
        max_steps=40,
    )

    history = await agent.run()

    # Copia screenshots generados por browser-use a artifacts/screens
    for src in history.screenshot_paths():
        try:
            shutil.copy2(src, screens_dir)
        except FileNotFoundError:
            pass

    # Guarda JSON de pantalla
    screen_json = run_dir / "screen.json"
    data: ScreenDescription = history.structured_output
    screen_json.write_text(json.dumps(data.model_dump(), indent=2, ensure_ascii=False))

    # Logs útiles en consola
    print("\n=== Artefactos ===")
    print("Visitadas:", history.urls())
    print("Screenshots guardados en:", screens_dir)
    print("Video dir:", video_dir)
    print("Traces dir:", traces_dir)
    print("HAR:", run_dir / "trace.har")
    print("Descripción JSON:", screen_json, "\n")

    # Asserts mínimos
    assert data.url.startswith("http"), f"URL inválida tras login: {data.url}"
    assert (data.title and len(data.title) > 0) or (data.h1 and len(data.h1) > 0), \
        f"Esperaba título o H1 tras login. JSON: {data.model_dump()}"
    # Evita que siga en la pantalla de login
    login_markers = ["Olvidé mi contraseña", "Iniciar sesión", "Regístrate"]
    assert not any(m in " ".join(data.primary_ctas + data.nav_items) for m in login_markers), \
        "Sigue en pantalla de login según elementos visibles."
