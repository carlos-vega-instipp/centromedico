# tests/integration/test_user_onboarding_flow.py
import re
import pytest
from django.urls import reverse
from django.core import mail
from django.test.client import Client
from urllib.parse import urlsplit
from django.contrib.auth.models import User
from autenticacion.models import Profile


@pytest.mark.django_db
def test_onboarding_crear_usuario_y_resetear_password(settings):
    """
    Flujo de integración:
    - Admin inicia sesión
    - Crea usuario con add-user (sin mocks)
    - Dispara reset de password para el nuevo usuario
    - Sigue link del correo y establece nueva contraseña
    - Hace login con la nueva contraseña
    """

    # Forzar backend de email en memoria para capturar correos
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    # 0) Crear admin y loguear
    admin_password = "Admin$1234"
    admin = User.objects.create_user(
        username="admin_test",
        email="admin@example.com",
        password=admin_password,
        is_staff=True,
        is_superuser=True,
        first_name="Admin",
        last_name="Test",
        is_active=True,
    )
    client = Client()
    assert client.login(username=admin.username, password=admin_password)

    # 1) Crear usuario vía la vista real `add-user`
    url_add = reverse("add-user")
    nuevo = {
        "txtUsername": "nuevo_user",
        "txtEmail": "nuevo@example.com",
        "txtNombres": "NUEVO",
        "txtApellidos": "USUARIO",
        "txtPassword": "IgnoradoPorLaVista",  # tu vista genera una temporal propia
        "txtCedula": "0955555555",
        "txtTelefono": "0999999999",
        "txtDireccion": "Calle Falsa 123",
        "txtFechaCumpleanos": "1990-01-01",
    }
    resp_add = client.post(url_add, nuevo, follow=True)
    assert resp_add.status_code in (200, 302)

    # 2) Verificar que el usuario y su perfil existen en la base
    assert User.objects.filter(username=nuevo["txtUsername"]).exists()
    u = User.objects.get(username=nuevo["txtUsername"])
    # si Profile está en otra app, ajusta el import/consulta
    assert Profile.objects.filter(user=u, cedula=nuevo["txtCedula"]).exists()

    # 3) Disparar reset de contraseña para ese usuario
    url_reset = reverse("password_reset")
    resp_reset = client.post(
        url_reset, {"email": nuevo["txtEmail"]}, follow=True)
    assert resp_reset.status_code == 200

    # 4) Capturar el último correo (puede haber correo de "bienvenida"; usamos el último)
    assert len(mail.outbox) >= 1
    email_body = mail.outbox[-1].body

    # 5) Extraer link (absoluto o relativo) a /reset/<uidb64>/<token>/
    m = re.search(r"https?://[^\s'\">]+/reset/\S+/\S+/", email_body)
    if not m:
        m = re.search(r"/reset/\S+/\S+/", email_body)
    assert m, f"No se encontró URL de confirmación en el correo:\n{email_body}"
    confirm_url = m.group(0)
    path = urlsplit(confirm_url).path

    # 6) Abrir link y seguir redirecciones hasta /set-password/
    resp_confirm_get = client.get(path, follow=True)
    assert resp_confirm_get.status_code == 200
    final_url = (
        resp_confirm_get.redirect_chain[-1][0]
        if resp_confirm_get.redirect_chain
        else resp_confirm_get.request.get("PATH_INFO")
    )
    assert final_url.endswith("/set-password/")

    # 7) Establecer nueva contraseña
    nueva_clave = "NuevaClave$123"
    resp_set = client.post(
        final_url,
        {"new_password1": nueva_clave, "new_password2": nueva_clave},
        follow=True,
    )
    assert resp_set.status_code == 200

    # 8) Login con la nueva contraseña en un cliente "limpio"
    client_fresco = Client()
    # tu vista de login espera inputUsername/inputPassword
    url_login = reverse("login")
    resp_login = client_fresco.post(
        url_login,
        {"inputUsername": nuevo["txtUsername"], "inputPassword": nueva_clave},
        follow=True,
    )
    assert resp_login.status_code == 200
    assert resp_login.wsgi_request.user.is_authenticated
