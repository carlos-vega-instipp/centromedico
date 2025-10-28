from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
import re

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nueva contraseña'
        }),
        help_text="Debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y un carácter especial."
    )
    new_password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu nueva contraseña'
        })
    )

    def clean_new_password1(self):
        password = self.cleaned_data.get("new_password1")
        errors = []

        # Verificar reglas personalizadas
        if len(password) < 8:
            errors.append("al menos 8 caracteres")
        if not re.search(r'[A-Z]', password):
            errors.append("una letra mayúscula")
        if not re.search(r'[a-z]', password):
            errors.append("una letra minúscula")
        if not re.search(r'[0-9]', password):
            errors.append("un número")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            errors.append("un carácter especial")

        # Si alguna regla falla → mostrar un solo mensaje unificado
        if errors:
            raise ValidationError(
                "La contraseña debe tener " + ", ".join(errors) + "."
            )
        
        return password
