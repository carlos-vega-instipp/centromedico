from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('list-users/', views.list_users, name='list-users'), 
    path('edit-user/<int:profile_id>/', views.edit_user, name='edit-user'), 
    path('delete-user/<int:profile_id>/', views.delete_user, name='delete-user'), 
]