import os
import time
import requests
import pytest

# Permite ajustar el SLA sin tocar el código: SLA_MS=2000 pytest -k perf
SLA_MS = int(os.getenv("SLA_MS", 2000))


@pytest.mark.perf
def test_login_page_latency_sla(live_server):
    """
    Verifica que la página de login responda por debajo del SLA.
    live_server es un fixture de pytest-django que levanta el server real.
    """
    url = f"{live_server.url}/autenticacion/login/"
    t0 = time.perf_counter()
    resp = requests.get(url, timeout=5)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    # 200 OK y debajo del umbral
    assert resp.status_code == 200, f"Status inesperado {resp.status_code} para {url}"
    assert elapsed_ms <= SLA_MS, f"Latencia {elapsed_ms:.1f} ms excede SLA {SLA_MS} ms"
