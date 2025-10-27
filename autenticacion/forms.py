from django.contrib.auth.forms import SetPasswordForm
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