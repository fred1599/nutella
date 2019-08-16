from django.urls import path
from .views import (
    LoginView, get_success_register, get_error_register,
    RegisterView, get_success_login, get_error_login
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/success/', get_success_register, name='success'),
    path('register/error/', get_error_register, name='error'),
    path('login/success/', get_success_login, name='success'),
    path('login/error/', get_error_login, name='error')
]