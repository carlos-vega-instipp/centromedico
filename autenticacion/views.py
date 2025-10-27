from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Q
import random
import string

# Create your views here.


def login_view(request):
    if request.method == 'GET':
        return render(request, 'autenticacion/login.html', {
            'error': None
        })
    else:
        user = authenticate(
            request, username=request.POST['inputUsername'], password=request.POST['inputPassword'])
        if user is None:
            return render(request, 'autenticacion/login.html', {
                'error': 'Usuario/email/cédula o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        cedula_ = request.POST['txtCedula']
        email_ = request.POST['txtEmail']
        username_ = request.POST['txtUsername']
        password_ = request.POST['txtPassword']
        first_name_ = request.POST['txtNombres']
        last_name_ = request.POST['txtApellidos']

        users = User.objects.filter(
            Q(username__iexact=username_) |
            Q(email__iexact=email_)
        )

        profiles = Profile.objects.filter(
            Q(cedula__iexact=cedula_)
        )

        if users.exists() or profiles.exists():
            return render(request, 'autenticacion/register.html', {
                'error': 'Ya existe un usuario con ese nombre de usuario, email o cédula'
            })
        else:
            userCreate = User.objects.create_user(
                username=username_, email=email_, password=password_, first_name=first_name_, last_name=last_name_)

            telefono_ = request.POST['txtTelefono']
            direccion_ = request.POST['txtDireccion']
            fechaCumpleanos_ = request.POST['txtFechaCumpleanos']
            profileCreate = Profile.objects.create(
                user=userCreate, cedula=cedula_, telefono=telefono_, direccion=direccion_, fecha_cumpleanos=fechaCumpleanos_)
            return render(request, 'autenticacion/login.html', {
                'message': 'Usuario creado correctamente. Ahora puedes iniciar sesión.'
            })

        return render(request, 'autenticacion/register.html')

    return render(request, 'autenticacion/register.html')


def recovery_password_view(request):
    if request.method == 'POST':
        email_ = request.POST.get('txtEmail')
        print(f"Email de recuperación solicitado para: {email_}")

        try:
            user = User.objects.get(email=email_)
            # Aquí iría la lógica para enviar el correo de recuperación
            password_generado = generar_contraseña()
            print(f"Contraseña generada para {email_}: {password_generado}")
            return render(request, 'autenticacion/login.html', {
                'message': 'Se ha enviado un correo de recuperación a su dirección de email.'
            })
        
        except User.DoesNotExist:
            return render(request, 'autenticacion/recovery-password.html', {
                'error': 'No existe ningún usuario con ese email.'
            })

    return render(request, 'autenticacion/recovery-password.html')


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
