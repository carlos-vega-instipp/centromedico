# tests/e2e/conftest.py
import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def _allow_sync_in_async():
    # Evita SynchronousOnlyOperation al correr con Playwright
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

# Para guardar los videos generados de la prueba e2e
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig):
    # Grabar video de cada test y guardar capturas en carpeta artifacts/
    return {
        **browser_context_args,
        "record_video_dir": "artifacts/videos",
        "viewport": {"width": 1280, "height": 800},
    }


@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    yield
    # Si falla el test, tomar screenshot
    if request.node.rep_call.failed:
        page.screenshot(path=f"artifacts/screenshots/{request.node.name}.png")
