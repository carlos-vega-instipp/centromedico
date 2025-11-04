import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
def test_add_user_calls_create_user_with_expected_fields(client_logged):
    """
    Parchea User.objects.create_user para verificar que se llama con:
    username, email, password, first_name, last_name.
    No toca la base de datos real.
    """
    url = reverse('add-user')
    post_data = {
        "txtUsername": "nuevo_user",
        "txtEmail": "nuevo@example.com",
        "txtNombres": "NUEVO",
        "txtApellidos": "USUARIO",
        "txtPassword": "Clave$1234",  # aunque se genera otra
        "txtCedula": "0955555555",
        "txtTelefono": "0999999999",
        "txtDireccion": "Calle Falsa 123",
        "txtFechaCumpleanos": "1990-01-01",
    }

    with patch("application.views.generar_contraseña", return_value="Clave$1234") as mock_gen, \
            patch("application.views.User.objects.create_user") as mock_create_user, \
            patch("application.views.Profile.objects.create") as mock_profile_create:
        # Simular que la creación retorna un "user" con id, por ejemplo
        fake_user = type("U", (), {"id": 1})
        mock_create_user.return_value = fake_user

        resp = client_logged.post(url, post_data, follow=True)
        assert resp.status_code == 200

        # 0) Se llamó al generador y se usó la password mockeada
        mock_gen.assert_called_once()

        # 1) create_user fue llamado con los kwargs esperados
        mock_create_user.assert_called_once()
        args, kwargs = mock_create_user.call_args
        assert kwargs["username"] == post_data["txtUsername"]
        assert kwargs["email"] == post_data["txtEmail"]
        assert kwargs["password"] == post_data["txtPassword"]
        assert kwargs["first_name"] == post_data["txtNombres"]
        assert kwargs["last_name"] == post_data["txtApellidos"]

        # 2) Profile.objects.create fue llamado con el user fake y los demás campos
        mock_profile_create.assert_called_once()
        _, pkwargs = mock_profile_create.call_args
        assert pkwargs["user"] is fake_user
        assert pkwargs["cedula"] == post_data["txtCedula"]
        assert pkwargs["telefono"] == post_data["txtTelefono"]
        assert pkwargs["direccion"] == post_data["txtDireccion"]
        assert str(pkwargs["fecha_cumpleanos"]
                   ) == post_data["txtFechaCumpleanos"]

        # 3) Verificar resultado esperado (redirect, mensaje, etc.)
        assert resp.status_code == 200
        # Puedes validar contenido de la plantilla de éxito si aplica
