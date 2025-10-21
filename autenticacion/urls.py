from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'), 
    path('logout/', views.logout_view, name='logout'), 
    path('recovery-password/', views.recovery_password_view, name='logout'), 
]