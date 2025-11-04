# tests/autenticacion/test_password_reset.py
import re
import pytest
from django.urls import reverse
from django.core import mail
from urllib.parse import urlsplit

@pytest.mark.django_db
def test_password_reset_success(client, user):
    # 1) Solicitar reset
    url = reverse("password_reset")
    resp = client.post(url, {"email": user.email}, follow=True)
    assert resp.status_code == 200

    # 2) Debe haberse enviado un correo
    assert len(mail.outbox) == 1, "No se envió el correo de reset"
    email_body = mail.outbox[0].body

    # 3) Extraer link (absoluto o relativo)
    m = re.search(r"https?://[^\s'\">]+/reset/\S+/\S+/", email_body)
    if not m:
        m = re.search(r"/reset/\S+/\S+/", email_body)
    assert m, f"No se encontró URL de confirmación en el correo:\n{email_body}"
    confirm_url = m.group(0)
    path = urlsplit(confirm_url).path  # nos quedamos con el path

    # 4) Abrir el link de confirmación y SEGUIR redirecciones
    resp_confirm_get = client.get(path, follow=True)
    # Debe resolver a la página final (set-password) con 200
    assert resp_confirm_get.status_code == 200

    # Obtener la URL final después del follow=True (debería terminar en /set-password/)
    # - opción A: desde la última redirección
    if resp_confirm_get.redirect_chain:
        final_url = resp_confirm_get.redirect_chain[-1][0]
    else:
        # - opción B: directamente del PATH_INFO
        final_url = resp_confirm_get.request.get("PATH_INFO")

    assert final_url.endswith("/set-password/"), f"URL final inesperada: {final_url}"
    html = resp_confirm_get.content.decode().lower()
    assert "new_password1" in html

    # 5) Enviar nuevas credenciales (POST) a la URL final
    new_pass = "NuevaClave!1"
    resp_confirm_post = client.post(final_url, {
        "new_password1": new_pass,
        "new_password2": new_pass,
    }, follow=True)
    assert resp_confirm_post.status_code == 200

    # 6) Login con la nueva clave
    login_url = reverse("login")
    # assert client.login(username=user.username, password=new_pass)
    resp_login = client.post(login_url, {"inputUsername": user.username, "inputPassword": new_pass}, follow=True)
    assert resp_login.status_code == 200

    # Opcional - Verificar que el usuario está autenticado
    assert resp_login.wsgi_request.user.is_authenticated
