from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

# Clase personalizada para agregar la clase form-control
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Iterar sobre los campos y agregar la clase CSS
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Nueva Contraseña', # Ayuda con el estilo
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Confirmar Contraseña', # Ayuda con el estilo
        })

# NUEVO: valida que el email exista
class CustomPasswordResetForm(PasswordResetForm):
    # (opcional) estiliza el input
    email = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        User = get_user_model()
        # Solo usuarios activos; ajusta si lo necesitas
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            # ← aquí forzamos el error visible en la plantilla
            raise ValidationError("El correo electrónico no se encuentra registrado.")
        return email