from body_mass_calculator.forms import MainDataForm
from body_mass_calculator.models import MainPersonData, BodyMassIndex
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

DEFAULT_BODY_MASS_INDEX = 0


class MainView(TemplateView):
    template_name = 'web/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['body_mass_index'] = DEFAULT_BODY_MASS_INDEX
        body_mass_index = BodyMassIndex.objects.filter(person=user)
        if body_mass_index.exists():
            context['body_mass_index'] = body_mass_index.first().value
        return context


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
