from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=False, null=True)
    fecha_cumpleanos = models.DateField(blank=False, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    cedula = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
