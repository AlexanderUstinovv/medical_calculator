from django.urls import path

from .views import LoginView

urlpatterns = [
    path(r'login/', LoginView.as_view(), name='form-login'),
#    path(r'sign-up/', '', name='form-registration')
]
