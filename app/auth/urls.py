from django.urls import path

from .views import LoginView, RegistrationView, SystemLogoutView

urlpatterns = [
    path(r'login/', LoginView.as_view(), name='form-login'),
    path(r'logout/', SystemLogoutView.as_view(), name='logout'),
    path(r'sign-up/', RegistrationView.as_view(), name='form-registration')
]
