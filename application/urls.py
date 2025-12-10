from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('add-user/', views.add_user, name='add-user'), 
    path('list-users/', views.list_users, name='list-users'), 
    path('edit-user/<int:profile_id>/', views.edit_user, name='edit-user'), 
    path('delete-user/<int:profile_id>/', views.delete_user, name='delete-user'),

    path('list-rols/', views.list_rols, name='list-rols'), 
    path('add-rol/', views.add_rol, name='add-rol'), 
    path('edit-rol/<int:rol_id>/', views.edit_rol, name='edit-rol'), 
    path('delete-rol/<int:rol_id>/', views.delete_rol, name='delete-rol'),

    path('list-permissions/', views.list_permissions, name='list-permissions'), 
    path('add-permission/', views.add_permission, name='add-permission'), 
    path('edit-permission/<int:permission_id>/', views.edit_permission, name='edit-permission'), 
    path('delete-permission/<int:permission_id>/', views.delete_permission, name='delete-permission'),
]