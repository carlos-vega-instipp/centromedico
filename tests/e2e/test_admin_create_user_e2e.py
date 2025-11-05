# tests/e2e/test_admin_creates_user_e2e.py
from django.urls import reverse
from django.contrib.auth.models import User
import pytest
pytestmark = pytest.mark.e2e

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.django_db
def test_admin_crea_usuario_por_ui(live_server, page):
    """
    E2E real con navegador (Playwright):
    - Crea admin en DB
    - Abre /login, inicia sesión por la UI (inputs reales)
    - Navega a "add-user", llena y envía el formulario
    - Verifica que el usuario quedó creado
    """
    # 0) Datos de admin y del nuevo usuario
    admin_pass = "Admin$1234"
    admin = User.objects.create_superuser(
        username="admin_test",
        email="admin@example.com",
        password=admin_pass,
        first_name="Admin",
        last_name="Test",
        is_active=True,
    )
    nuevo = {
        "txtUsername": "nuevo_user",
        "txtEmail": "nuevo@example.com",
        "txtNombres": "NUEVO",
        "txtApellidos": "USUARIO",
        "txtPassword": "IgnoradoPorLaVista",
        "txtCedula": "0955555555",
        "txtTelefono": "0999999999",
        "txtDireccion": "Calle Falsa 123",
        "txtFechaCumpleanos": "1990-01-01",
    }

    # 1) Login por la UI
    login_url = live_server.url + reverse("login")
    page.goto(login_url)

    # Tu vista espera "inputUsername" y "inputPassword"
    page.fill('input[name="inputUsername"]', admin.username)
    page.fill('input[name="inputPassword"]', admin_pass)
    page.click('input[type="submit"]')

    # Puedes esperar alguna señal post-login (titulo, texto, URL, etc.)
    # Si redirige a home:
    # page.wait_for_url("**/home")

    # 2) Ir a la página "add-user" y llenar form
    add_user_url = live_server.url + reverse("add-user")
    page.goto(add_user_url)

    page.fill('input[name="txtUsername"]', nuevo["txtUsername"])
    page.fill('input[name="txtEmail"]', nuevo["txtEmail"])
    page.fill('input[name="txtNombres"]', nuevo["txtNombres"])
    page.fill('input[name="txtApellidos"]', nuevo["txtApellidos"])
    page.fill('input[name="txtCedula"]', nuevo["txtCedula"])
    page.fill('input[name="txtTelefono"]', nuevo["txtTelefono"])
    page.fill('input[name="txtDireccion"]', nuevo["txtDireccion"])
    page.fill('input[name="txtFechaCumpleanos"]', nuevo["txtFechaCumpleanos"])

    # Envía el formulario (ajusta el selector del botón según tu template)
    page.click('input[type="submit"]')

    # 3) Verificación de resultado:
    #    a) Por UI: busca un texto de éxito o que aparezca en una tabla/lista
    #       Si tienes una lista de usuarios en la misma página o tras redirección:
    # page.wait_for_selector(f"text={nuevo['txtUsername']}")

    #    b) Por backend (DB): confirma que el usuario fue creado
    assert User.objects.filter(username=nuevo["txtUsername"]).exists()
