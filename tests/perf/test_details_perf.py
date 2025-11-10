# test_mejorado.py - Para diagnosticar dónde está el cuello de botella
import time
import requests
import pytest


def test_login_latency_detailed(live_server):
    url = f"{live_server.url}/autenticacion/login/"

    # Medición DNS + Conexión + Transferencia
    t0 = time.perf_counter()
    resp = requests.get(url, timeout=10)
    total_time = (time.perf_counter() - t0) * 1000

    # Tiempo hasta primer byte (TTFB)
    ttfb = resp.elapsed.total_seconds() * 1000

    print(f"\n=== DIAGNÓSTICO DETALLADO ===")
    print(f"Tiempo total: {total_time:.1f} ms")
    print(f"TTFB (Time To First Byte): {ttfb:.1f} ms")
    print(f"Tamaño respuesta: {len(resp.content)} bytes")
    print(f"Headers: {dict(resp.headers)}")

    assert resp.status_code == 200
