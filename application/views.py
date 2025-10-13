from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from autenticacion.models import Profile
from django.contrib.auth.models import User

# Create your views here.
@login_required
def home(request):
    return render(request, 'application/home.html')

@login_required
def list_users(request):
    perfiles = Profile.objects.all()
    return render(request, 'application/list-users.html', {
        'perfiles': perfiles
    })

@login_required
def edit_user(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        #user
        profile.user.first_name = request.POST.get('txtNombres')
        profile.user.last_name = request.POST.get('txtApellidos')
        profile.user.email = request.POST.get('txtEmail')
        
        #profile
        profile.cedula = request.POST.get('txtCedula')        
        profile.telefono = request.POST.get('txtTelefono')
        profile.direccion = request.POST.get('txtDireccion')
        profile.user.save()
        profile.save()
        return render(request, 'application/list-users.html', {
            'perfiles': Profile.objects.all()
        })
    return render(request, 'application/edit-user.html', {'profile': profile})

@login_required
def delete_user(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        user = User.objects.get(id=profile.user.id)
        user.delete()
        return render(request, 'application/list-users.html', {
            'perfiles': Profile.objects.all()
        })
    return render(request, 'application/delete-user.html', {'profile': profile})