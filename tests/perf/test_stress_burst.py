import os
import math
import time
import requests
import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed

USERS = int(os.getenv("BURST_USERS", "20"))          # hilos concurrentes
REQUESTS = int(os.getenv("BURST_REQUESTS", "100"))   # total de requests
P95_MS = int(os.getenv("P95_MS", "2500"))            # umbral p95
ERROR_RATE_MAX = float(os.getenv("ERROR_RATE_MAX", "0.05"))  # 5%


def percentile(values, p):
    """Retorna el percentil p (0-100) de una lista no vacía."""
    if not values:
        return math.nan
    values = sorted(values)
    k = (len(values)-1) * (p/100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return values[int(k)]
    return values[f] + (values[c] - values[f]) * (k - f)


@pytest.mark.perf
def test_burst_stress_login(live_server):
    """
    Ráfaga concurrente de requests a una ruta (GET) para medir estabilidad bajo carga breve.
    Apta para CI (no bloqueante, < ~10s).
    """
    url = f"{live_server.url}/autenticacion/login/"

    latencies = []
    errors = 0

    def shoot(_):
        t0 = time.perf_counter()
        try:
            r = requests.get(url, timeout=5)
            ok = (200 <= r.status_code < 400)
        except Exception:
            ok = False
        dt = (time.perf_counter() - t0) * 1000
        return ok, dt

    with ThreadPoolExecutor(max_workers=USERS) as ex:
        futures = [ex.submit(shoot, i) for i in range(REQUESTS)]
        for fut in as_completed(futures):
            ok, ms = fut.result()
            if ok:
                latencies.append(ms)
            else:
                errors += 1

    total = REQUESTS
    error_rate = errors / total
    p95 = percentile(latencies, 95) if latencies else float("inf")
    avg = sum(latencies) / len(latencies) if latencies else float("inf")

    # Asserts “no funcionales” básicos
    assert error_rate <= ERROR_RATE_MAX, f"Error rate {error_rate:.1%} > {ERROR_RATE_MAX:.1%}"
    assert p95 <= P95_MS, f"p95 {p95:.1f} ms > {P95_MS} ms (avg {avg:.1f} ms, errors {errors}/{total})"
