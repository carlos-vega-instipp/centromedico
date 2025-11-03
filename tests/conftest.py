# tests/conftest.py
import pytest
from django.contrib.auth.models import User
from django.test.client import Client
from django.conf import settings


@pytest.fixture(autouse=True)
def _email_backend_locmem(settings):
    """
    Usar el backend de memoria para capturar correos en tests.
    """
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture
def user_data():
    return {
        "username": "test1",
        "email": "carlos.vega@instipp.edu.ec",
        "password": "Cv123456789!",
        "first_name": "First name test",
        "last_name": "Las name test",
    }


@pytest.fixture
@pytest.mark.django_db
def user(django_user_model, user_data):
    return django_user_model.objects.create_user(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        is_active=True,
    )


@pytest.fixture
@pytest.mark.django_db
def client_logged(user):
    client = Client()
    assert client.login(username=user.username, password="Cv123456789!")
    return client
