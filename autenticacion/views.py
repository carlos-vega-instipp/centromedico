from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Q

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
