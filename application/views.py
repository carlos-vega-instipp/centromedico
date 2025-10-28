from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from autenticacion.models import Profile
from django.contrib.auth.models import User
import random
import string

# Create your views here.


@login_required
def home(request):
    return render(request, 'application/home.html')


@login_required
def list_users(request):
    perfiles = Profile.objects.all()
    return render(request, 'application/list-users.html', {
        'perfiles': perfiles
    })


@login_required
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

        print("Contraseña generada: ", password_)

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
        return redirect('list-users')
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


def generar_contraseña():
    # Definir los conjuntos de caracteres
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    especiales = '@.!_$'

    # Asegurar al menos un carácter de cada tipo
    contrasena = [
        random.choice(mayusculas),
        random.choice(minusculas),
        random.choice(numeros),
        random.choice(especiales)
    ]

    # Completar hasta 8 caracteres con caracteres aleatorios de todos los tipos
    todos_caracteres = mayusculas + minusculas + numeros + especiales
    contrasena.extend(random.choice(todos_caracteres) for _ in range(4))

    # Mezclar la contraseña
    random.shuffle(contrasena)

    return ''.join(contrasena)

