from django.urls import path, re_path
from users.views import *
from django.contrib.auth import views as auth

urlpatterns = [
    re_path(r'^registration$', RegistrationView.as_view(), name='registration_url'),
    re_path(r'^signin$', auth.LoginView.as_view(template_name='users/signin.html'), name='signin_url'),
    re_path(r'^signout$', auth.LogoutView.as_view(template_name='users/signout.html'), name='signout_url'),
    re_path(r'^profile$', ProfileView.as_view(), name='profile_url'),
    path('validate_username/', validate_username),
]