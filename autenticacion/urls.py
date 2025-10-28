from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'), 
    path('logout/', views.logout_view, name='logout'), 

    # --- Vistas de recuperación de contraseña ---
    path('password/', views.password_view, name='password'),
    path('reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('reset/confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
]
