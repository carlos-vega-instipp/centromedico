from django.urls import path
from . import views
from .forms import CustomSetPasswordForm, CustomPasswordResetForm
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'), 
    path('logout/', views.logout_view, name='logout'), 
    # 2.1 Pide el correo electrónico (Usaremos tu plantilla 'password_reset_form.html')
    path(
        'password_reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='autenticacion/password_reset_form.html', # La plantilla que pide el email
            email_template_name='autenticacion/password_reset_email.html', # El contenido del correo
            subject_template_name='autenticacion/password_reset_subject.txt', # El asunto
            success_url='done/', # Redirecciona a la ruta 'password_reset_done' definida abajo,
            form_class=CustomPasswordResetForm # <-- Aquí asignamos tu formulario
        ), 
        name='password_reset'
    ),
    
    # 2.2 Mensaje de éxito tras enviar el correo
    path(
        'password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='autenticacion/password_reset_done.html' # Plantilla que informa que se envió el correo
        ), 
        name='password_reset_done'
    ),
    
    # 2.3 Formulario para ingresar la nueva contraseña (Contiene el token y uidb64)
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='autenticacion/password_reset_confirm.html',
             form_class=CustomSetPasswordForm # <-- Aquí asignamos tu formulario
         ), 
         name='password_reset_confirm'
    ),
    
    # 2.4 Confirmación final (Contraseña cambiada con éxito)
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='autenticacion/password_reset_complete.html' # Plantilla de éxito final
        ), 
        name='password_reset_complete'
    ),
]