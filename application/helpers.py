# application/helpers.py

from django.contrib.auth.models import User

def is_admin(user: User) -> bool:
    """
    Devuelve True si el usuario es administrador.
    Se puede cambiar la lógica aquí si luego usas grupos o perfiles.
    """
    return user.is_superuser