from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Q

from django.contrib.auth.views import PasswordResetView
from django.contrib import messages

from django.contrib.auth.views import PasswordResetConfirmView
from .forms import CustomSetPasswordForm
from django.urls import reverse_lazy

# Create your views here.


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'autenticacion/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'autenticacion/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = '/autenticacion/password_reset/done/'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ingresado no está registrado en el sistema.')
            return redirect('password_reset')  # Nombre del path de la URL
        return super().post(request, *args, **kwargs)

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

# def resetear_pass(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name="autenticacion/password_reset_email.html",
                )
                messages.success(request, "Se ha enviado un enlace a su correo.")
        else:
            messages.error(request, "El correo no está registrado.")
    return render(request, "autenticacion/password_reset.html")
