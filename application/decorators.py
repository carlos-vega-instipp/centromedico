from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from autenticacion.models import UserGroupExtra

def group_required(*groups_names):
    """
    Requiere que el usuario tenga al menos uno de los grupos indicados
    Y que esa asignación esté activa (estado=True) en UserGroupExtra.
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            if not user.is_authenticated:
                return redirect('login')
            
            # Se busca alguna asignación activa de esos grupos
            tiene_rol = UserGroupExtra.objects.filter(
                user=user,
                group__name__in=groups_names,
                estado=True
            ).exists()

            if tiene_rol:
                return view_func(request, *args, **kwargs)

            return redirect(reverse('no-permission'))

        return _wrapped_view
    return decorator