from django import template
from autenticacion.models import UserGroupExtra

register = template.Library()

@register.filter
def has_group(user, group_name):
    """
    Verifica si el usuario pertenece a un grupo específico
    y que esa asignación esté activa (estado=True) en UserGroupExtra.

    Uso en plantilla:
    {% if user|has_group:"ADMINISTRADOR" %}
        ...
    {% endif %}
    """
    if user.is_superuser:
        return True

    return UserGroupExtra.objects.filter(
        user=user,
        group__name=group_name,
        estado=True
    ).exists()