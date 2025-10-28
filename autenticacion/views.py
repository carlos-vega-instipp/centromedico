import random
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def login_view(request):
    if request.method == 'GET':
        return render(request, 'autenticacion/login.html', {'error': None})
    
    username_or_email = request.POST.get('inputUsername')
    password = request.POST.get('inputPassword')

    # Buscar si el usuario ingresó un correo
    try:
        user_obj = User.objects.get(email=username_or_email)
        username = user_obj.username
    except User.DoesNotExist:
        username = username_or_email  # Asumimos que ingresó su username directamente

    # Autenticar al usuario
    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, 'autenticacion/login.html', {
            'error': 'Usuario, correo o contraseña incorrectos.'
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


def verify_code_view(request):
    # Lógica para enviar código al correo
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Enviar código por correo
            ...
            return render(request, 'autenticacion/verify_code.html', {'email': email})
        except User.DoesNotExist:
            return render(request, 'autenticacion/password.html', {'error': 'Correo no registrado'})
    return render(request, 'autenticacion/password.html')

def password_view(request):
    step = request.session.get('step', 'email')  # email, verify, change

    if request.method == 'POST':
        # Paso 1: enviar código
        if 'send_code' in request.POST:
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'autenticacion/password.html', {'error': 'Email no existe', 'step': 'email'})
            except User.MultipleObjectsReturned:
                return render(request, 'autenticacion/password.html', {'error': 'Varios usuarios con ese email', 'step': 'email'})

            code = str(random.randint(100000, 999999))
            request.session['password_code'] = code
            request.session['password_user'] = user.id
            request.session['step'] = 'verify'

            send_mail(
                'Código de recuperación',
                f'Tu código es: {code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            return render(request, 'autenticacion/password.html', {'message': 'Código enviado', 'step': 'verify'})

        # Paso 2: verificar código
        elif 'verify_code' in request.POST:
            if request.POST.get('code') == request.session.get('password_code'):
                request.session['step'] = 'change'
                return render(request, 'autenticacion/password.html', {'message': 'Código correcto', 'step': 'change'})
            else:
                return render(request, 'autenticacion/password.html', {'error': 'Código incorrecto', 'step': 'verify'})

        # Paso 3: cambiar contraseña
        elif 'change_password' in request.POST:
            new_pass = request.POST.get('new_password')
            confirm = request.POST.get('confirm_password')
            if new_pass != confirm:
                return render(request, 'autenticacion/password.html', {'error': 'Contraseñas no coinciden', 'step': 'change'})

            user_id = request.session.get('password_user')
            user = User.objects.get(id=user_id)
            user.set_password(new_pass)
            user.save()

            # Limpiar sesión
            for k in ['password_code', 'password_user', 'step']:
                request.session.pop(k, None)

            return render(request, 'autenticacion/login.html', {'message': 'Contraseña cambiada. Inicia sesión.'})

    return render(request, 'autenticacion/password.html', {'step': step})

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Envías el código al correo...
            request.session['recovery_email'] = email  # <--- GUARDAS EL CORREO EN SESIÓN
            return redirect('verify_code')
        else:
            messages.error(request, "El correo no está registrado.")
    return render(request, 'autenticacion/password.html')




