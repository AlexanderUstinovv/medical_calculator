from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views.generic import FormView


class LoginView(FormView):
    template_name = 'auth/login_form.html'
    form_class = AuthenticationForm
    # TODO: change it to url resolve
#    success_url = reverse('main')
    success_url = '/main/'


class RegistrationView(FormView):
    template_name = 'auth/registration_form.html'
    form_class = UserCreationForm
    # TODO: change it to url resolve
#    success_url = reverse('main')
    success_url = '/main/'