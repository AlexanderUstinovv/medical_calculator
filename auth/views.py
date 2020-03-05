from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView


class LoginView(FormView):
    template_name = 'auth/login_form.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('web:main')

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=name, password=password)
            if user.is_active:
                login(request, user)
                return super().post(request, *args, **kwargs)
            else:
                raise ValidationError('Account is not activated')
        else:
            raise ValidationError('Authentication failed')


class SystemLogoutView(LogoutView):
    next_page = reverse_lazy('auth:form-login')


class RegistrationView(FormView):
    # TODO: check how it works
    template_name = 'auth/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('web:main')
