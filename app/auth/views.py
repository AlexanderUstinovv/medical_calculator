from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

MAIN_PAGE = reverse_lazy('web:main')


class LoginView(FormView):
    template_name = 'auth/login_form.html'
    form_class = AuthenticationForm
    success_url = MAIN_PAGE

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(MAIN_PAGE)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect(self.get_success_url())
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=name, password=password)
            if user.is_active:
                login(request, user)
                return self.form_valid(form)
        return self.form_invalid(form)


class SystemLogoutView(LogoutView):
    next_page = reverse_lazy('auth:form-login')


class RegistrationView(FormView):
    template_name = 'auth/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('auth:form-login')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(MAIN_PAGE)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            password_1 = form.cleaned_data.get('password1')
            password_2 = form.cleaned_data.get('password2')
            user_in_db = User.objects.filter(username=name)
            if not user_in_db.exists() and password_1 == password_2:
                user = User(username=name)
                user.set_password(password_1)
                user.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
