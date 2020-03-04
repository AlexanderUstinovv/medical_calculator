from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from body_mass_calculator.forms import MainDataForm
from body_mass_calculator.models import MainPersonData


def main(request):
    return render(request, 'web/base.html')


class MainDataView(FormView):
    template_name = 'web/forms/main_data_form.html'
    success_url = reverse_lazy('web:main')
    form_class = MainDataForm

    # TODO: fix form validation
    def form_valid(self, form):
        user = self.request.user
        form_data = form.cleaned_data
        person_data = MainPersonData.objects.filter(person=user)
        if person_data.exists():
            person_data.update(
                name=form_data.get('name'),
                age=form_data.get('age'),
                sex=form_data.get('sex'),
                height=form_data.get('height'),
                weight=form_data.get('weight')
            )
        else:
            MainPersonData.objects.create(
                person=user,
                name=form_data.get('name'),
                age=form_data.get('age'),
                sex=form_data.get('sex'),
                height=form_data.get('height'),
                weight=form_data.get('weight')
            )
        return super().form_valid(form)
