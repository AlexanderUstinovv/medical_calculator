from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.views.generic import FormView


class LoginView(FormView):
    template_name = 'auth/login_form.html'
    form_class = AuthenticationForm
#    success_url = reverse('main')
    success_url = '/main/'
