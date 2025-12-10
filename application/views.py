from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import group_required
from autenticacion.models import Profile, UserGroupExtra
from django.contrib.auth.models import User, Group, Permission
from .utils import generar_contraseña
from django.core.mail import send_mail
from .helpers import is_admin

# Create your views here.


@login_required
def home(request):
    return render(request, 'application/home.html')


@login_required
@user_passes_test(is_admin, login_url='no-permission')
@group_required('ADMINISTRADOR')
def list_users(request):
    perfiles = Profile.objects.all()
    return render(request, 'application/list-users.html', {
        'perfiles': perfiles
    })


@login_required
@group_required('ADMINISTRADOR')
def add_user(request):
    if request.method == 'POST':

        # user
        username_ = request.POST.get('txtUsername')
        email_ = request.POST.get('txtEmail')
        first_name_ = request.POST.get('txtNombres').upper()
        last_name_ = request.POST.get('txtApellidos').upper()
        password_ = generar_contraseña()

        # profile
        cedula_ = request.POST.get('txtCedula')
        telefono_ = request.POST.get('txtTelefono')
        direccion_ = request.POST.get('txtDireccion')
        fechaCumpleanos_ = request.POST.get('txtFechaCumpleanos')

        # Validaciones que no exista el user ni el profile
        if User.objects.filter(username=username_).exists():
            error_message = "El nombre de usuario ya existe."
            return render(request, 'application/add-user.html', {'error': error_message})

        if User.objects.filter(email=email_).exists():
            error_message = "El email del usuario ya existe"
            return render(request, 'application/add-user.html', {'error': error_message})

        if Profile.objects.filter(cedula=cedula_).exists():
            error_message = "La cédula del usuario ya existe"
            return render(request, 'application/add-user.html', {'error': error_message})

        # Crear user y profile
        userCreate = User.objects.create_user(
            username=username_, email=email_, password=password_, first_name=first_name_, last_name=last_name_)

        profileCreate = Profile.objects.create(
            user=userCreate,
            cedula=cedula_,
            telefono=telefono_,
            direccion=direccion_,
            fecha_cumpleanos=fechaCumpleanos_
        )

        # Enviar correo con la contraseña generada
        send_mail(
            subject='Creación de usuario nuevo con contraseña generada',
            message=f"Se ha creado un usuario con username {username_} y contraseña {password_}. Por favor, cambie su contraseña después de iniciar sesión.",
            from_email=None,  # usa DEFAULT_FROM_EMAIL
            recipient_list=[email_],
            fail_silently=False,
        )

        return render(request, 'application/list-users.html', {
            'perfiles': Profile.objects.all(),
            'mensaje': 'Usuario creado correctamente.'
        })
    return render(request, 'application/add-user.html')


@login_required
def edit_user(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        # user
        profile.user.first_name = request.POST.get('txtNombres').upper()
        profile.user.last_name = request.POST.get('txtApellidos').upper()
        profile.user.email = request.POST.get('txtEmail')
        profile.user.is_active = request.POST.get('switchCheck') == 'on'

        # profile
        profile.cedula = request.POST.get('txtCedula')
        profile.telefono = request.POST.get('txtTelefono')
        profile.direccion = request.POST.get('txtDireccion')
        profile.user.save()
        profile.save()
        return render(request, 'application/list-users.html', {
            'perfiles': Profile.objects.all(),
            'mensaje': 'Usuario actualizado correctamente.'
        })
    return render(request, 'application/edit-user.html', {'profile': profile})


@login_required
def delete_user(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        user = User.objects.get(id=profile.user.id)
        user.delete()
        return render(request, 'application/list-users.html', {
            'perfiles': Profile.objects.all()
        })
    return render(request, 'application/delete-user.html', {'profile': profile})

# =========================================================
# GESTIÓN DE ROLES
# =========================================================


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def list_rols(request):
    roles = Group.objects.all()
    return render(request, 'application/list-rols.html', {
        'roles': roles
    })


@login_required
def add_rol(request):
    if request.method == 'POST':

        nombreRol = request.POST.get('txtNombreRol')
        # Validaciones que no exista el rol ni el profile
        if Group.objects.filter(name__iexact=nombreRol).exists():
            error_message = "El nombre del rol ya existe."
            return render(request, 'application/add-rol.html', {'error': error_message})

        # Crear el rol
        rolCreate = Group.objects.create(name=nombreRol.upper())

        return render(request, 'application/list-rols.html', {
            'roles': Group.objects.all(),
            'mensaje': 'Rol creado correctamente.'
        })
    return render(request, 'application/add-rol.html')


@login_required
def edit_rol(request, rol_id):
    rol = Group.objects.get(id=rol_id)
    if request.method == 'POST':
        # user
        rol.name = request.POST.get('txtNombreRol').upper()
        rol.save()
        return render(request, 'application/list-rols.html', {
            'roles': Group.objects.all(),
            'mensaje': 'Rol actualizado correctamente.'
        })
    return render(request, 'application/edit-rol.html', {'rol': rol})


@login_required
def delete_rol(request, rol_id):
    rol = Group.objects.get(id=rol_id)
    if request.method == 'POST':
        rol.delete()
        return render(request, 'application/list-rols.html', {
            'roles': Group.objects.all(),
            'mensaje': 'Rol eliminado correctamente.'
        })
    return render(request, 'application/delete-rol.html', {'rol': rol})

# =========================================================
# GESTIÓN DE PERMISOS (roles con usuarios asignados)
# =========================================================


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def list_permissions(request):
    permisos = UserGroupExtra.objects.all().order_by('-fecha_asignacion')
    return render(request, 'application/list-permissions.html', {
        'permisos': permisos
    })


@login_required
def add_permission(request):
    if request.method == 'POST':

        rol_id = request.POST.get('rol_id')
        user_id = request.POST.get('usuario_id')

        rol = Group.objects.get(id=rol_id)
        user = User.objects.get(id=user_id)

        if UserGroupExtra.objects.filter(group=rol, user=user).exists():
            error_message = "El registro ya existe."
            return render(request, 'application/add-permission.html', {'error': error_message})

        # Crear el registro en UserGroupExtra y UserGroup de Django
        user.groups.add(rol)

        permissionCreate = UserGroupExtra.objects.update_or_create(
            group=rol, user=user, estado=True)

        return render(request, 'application/list-permissions.html', {
            'permisos': UserGroupExtra.objects.all().order_by('-fecha_asignacion'),
            'mensaje': 'Permiso creado correctamente.'
        })
    return render(request, 'application/add-permission.html')


def edit_permission(request, permission_id):
    permission = UserGroupExtra.objects.get(id=permission_id)

    if request.method == 'POST':

        rol_id = request.POST.get('rol_id')
        user_id = request.POST.get('usuario_id')

        rol = Group.objects.get(id=rol_id)
        user = User.objects.get(id=user_id)

        if UserGroupExtra.objects.filter(user=user, group=rol).exists():
            error_message = "El permiso de ese usuario con el rol ya existe."
            return render(request, 'application/edit-permission.html', {'error': error_message, 'permission': permission})

        user.groups.remove(permission.group)

        try:
            uge = UserGroupExtra.objects.get(id=permission_id)
            uge.user = user
            uge.group = rol
            uge.fecha_asignacion = timezone.now()
            uge.save()

            user.groups.add(rol)
        except UserGroupExtra.DoesNotExist:
            pass
        
        permisos = UserGroupExtra.objects.all().order_by('-fecha_asignacion')
        
        return render(request, 'application/list-permissions.html', {
            'permisos': permisos,
            'mensaje': 'Permiso actualizado correctamente.'
        })
    return render(request, 'application/edit-permission.html', {'permission': permission})

@login_required
def delete_permission(request, permission_id):
    uge = UserGroupExtra.objects.get(id=permission_id)
    user = uge.user
    if request.method == 'POST':
        user.groups.remove(uge.group)
        uge.delete()

        permisos = UserGroupExtra.objects.all().order_by('-fecha_asignacion')
        return render(request, 'application/list-permissions.html', {
            'permisos': permisos,
            'mensaje': 'Permiso eliminado correctamente.'
        })
    return render(request, 'application/delete-permission.html', {'permission': uge})