from django.urls import path

from .views import LoginView, RegistrationView

urlpatterns = [
    path(r'login/', LoginView.as_view(), name='form-login'),
    path(r'sign-up/', RegistrationView.as_view(), name='form-registration')
]
