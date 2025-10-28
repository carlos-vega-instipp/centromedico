from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
import random
import string
from .models import Profile
from django.utils import timezone


# --- LOGIN ---
def login_view(request):
    if request.method == 'GET':
        return render(request, 'autenticacion/login.html', {'error': None})

    input_value = request.POST['inputUsername']
    password = request.POST['inputPassword']

    # Buscar usuario por username, email o cédula
    try:
        user = User.objects.get(Q(username=input_value) | Q(email=input_value) | Q(profile__cedula=input_value))
    except User.DoesNotExist:
        return render(request, 'autenticacion/login.html', {
            'error': 'Este correo o usuario no está asociado a ninguna cuenta.'
        })

    # Autenticar usuario
    user_auth = authenticate(request, username=user.username, password=password)

    if user_auth is None:
        profile = Profile.objects.filter(user=user).first()
        if profile and profile.temp_password == password:
            login(request, user)
            messages.info(request, 'Has iniciado sesión con una contraseña temporal. Cámbiala ahora.')
            return redirect('password_reset_confirm')
        else:
            return render(request, 'autenticacion/login.html', {
                'error': 'Usuario/email/cédula o contraseña incorrectos.'
            })

    login(request, user_auth)
    messages.success(request, 'Has iniciado sesión correctamente.')
    return redirect('home')


# --- LOGOUT ---
def logout_view(request):
    logout(request)
    return redirect('login')


# --- REGISTRO ---
def register_view(request):
    if request.method == 'POST':
        cedula_ = request.POST['txtCedula']
        email_ = request.POST['txtEmail']
        username_ = request.POST['txtUsername']
        password_ = request.POST['txtPassword']
        first_name_ = request.POST['txtNombres']
        last_name_ = request.POST['txtApellidos']

        if User.objects.filter(Q(username=username_) | Q(email=email_)).exists() or Profile.objects.filter(Q(cedula=cedula_)).exists():
            return render(request, 'autenticacion/register.html', {
                'error': 'Ya existe un usuario con ese nombre de usuario, email o cédula.'
            })

        userCreate = User.objects.create_user(
            username=username_,
            email=email_,
            password=password_,
            first_name=first_name_,
            last_name=last_name_
        )

        telefono_ = request.POST['txtTelefono']
        direccion_ = request.POST['txtDireccion']
        fechaCumpleanos_ = request.POST['txtFechaCumpleanos']

        Profile.objects.create(
            user=userCreate,
            cedula=cedula_,
            telefono=telefono_,
            direccion=direccion_,
            fecha_cumpleanos=fechaCumpleanos_
        )

        return render(request, 'autenticacion/login.html', {
            'message': 'Usuario creado correctamente. Ahora puedes iniciar sesión.'
        })

    return render(request, 'autenticacion/register.html')


# --- RECUPERAR CONTRASEÑA ---
def password_view(request):
    if request.method == 'POST':
        correo = request.POST.get('email')
        try:
            usuario = User.objects.get(email=correo)

            # Generar contraseña temporal
            temporal = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            usuario.set_password(temporal)
            usuario.save()

            # Enviar correo
            send_mail(
                'Recuperación de contraseña',
                f'Hola {usuario.username},\n\n'
                f'Tu contraseña temporal es: {temporal}\n'
                f'Usa este enlace para restablecer tu contraseña:\n'
                f'http://127.0.0.1:8000/reset/confirm/\n\n'
                f'Esta contraseña temporal expirará en 10 minutos.\n\n'
                f'Atentamente,\nEl equipo de soporte',
                'tucorreo@gmail.com',
                [correo],
                fail_silently=False,
            )

            messages.success(request, 'Se ha enviado una contraseña temporal a tu correo.')
            return redirect('password_reset_done')

        except User.DoesNotExist:
            messages.error(request, 'No existe un usuario con ese correo electrónico.')

    return render(request, 'autenticacion/password.html')



def password_reset_confirm_view(request):
    if request.method == 'POST':
        temp_password = request.POST.get('temp_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión con tu contraseña temporal primero.")
            return redirect('login')

        user = request.user

        if not user.check_password(temp_password):
            messages.error(request, "La contraseña temporal no es válida.")
            return redirect('password_reset_confirm')

        if new_password != confirm_password:
            messages.error(request, "Las contraseñas nuevas no coinciden.")
            return redirect('password_reset_confirm')

        # ✅ Cambia la contraseña
        user.set_password(new_password)
        user.save()

        messages.success(request, "Tu contraseña ha sido actualizada con éxito.")

        # ✅ Redirige al template de "contraseña restablecida"
        return redirect('password_reset_confirm')

    return render(request, 'autenticacion/password_reset_confirm.html')

# --- CONFIRMACIÓN DE ENVÍO DE CORREO ---
def password_reset_done_view(request):
    """Muestra la página que confirma que el correo de restablecimiento fue enviado."""
    return render(request, 'autenticacion/password_reset_done.html')

# --- MENSAJE FINAL DE ÉXITO ---
def password_reset_complete_view(request):
    """Muestra la página final después de restablecer la contraseña correctamente."""
    return render(request, 'autenticacion/password_reset_complete.html')
