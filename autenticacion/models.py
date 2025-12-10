from django.db import models
from django.contrib.auth.models import User, Group

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=False, null=True)
    fecha_cumpleanos = models.DateField(blank=False, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    cedula = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class UserGroupExtra(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles_extra')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='users_extra')

    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'group')
        verbose_name = 'Asignación de rol'
        verbose_name_plural = 'Asignaciones de roles'

    def __str__(self):
        return f"{self.user.username} - {self.group.name} (activo={self.estado})"
    
