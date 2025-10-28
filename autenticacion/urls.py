from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('login/', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'), 
    path('logout/', views.logout_view, name='logout'), 
    path('password/', views.password_view, name='password'), 
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('verify-code/', views.verify_code_view, name='verify_code'),

]