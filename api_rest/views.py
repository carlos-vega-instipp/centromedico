from django.contrib.auth.models import Group, User
from autenticacion.models import Profile
from rest_framework import permissions, viewsets, filters

from .serializers import GroupSerializer, UserSerializer, ProfileSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    
    # --- AGREGAR ESTAS DOS LÍNEAS ---
    filter_backends = [filters.SearchFilter]
    
    search_fields = ['first_name', 'last_name']

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]

     # --- AGREGAR ESTAS DOS LÍNEAS ---
    filter_backends = [filters.SearchFilter]
    
    search_fields = ['name']

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [permissions.IsAuthenticated]