from body_mass_calculator.forms import MainDataForm
from body_mass_calculator.models import MainPersonData, BodyMassIndex
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from medical_test.form_generator import generate_form_by_recommendation
from medical_test.models import MedicalProcedure
from medical_test.recommendations import recommend_medical_test

DEFAULT_BODY_MASS_INDEX = 0


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'web/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['body_mass_index'] = DEFAULT_BODY_MASS_INDEX
        body_mass_index = BodyMassIndex.objects.filter(person=user)
        if body_mass_index.exists():
            context['body_mass_index'] = body_mass_index.first().value
        main_data = MainPersonData.objects.filter(person=user)
        context['recommended'] = []
        if main_data.exists():
            recommended = recommend_medical_test(main_data.first().sex,
                                                 main_data.first().age)
            for item in recommended:
                context['recommended'].append(
                    {'name': item.name, 'id': item.id})
        return context


class MainDataView(LoginRequiredMixin, FormView):
    template_name = 'web/forms/main_data_form.html'
    success_url = reverse_lazy('web:main')
    form_class = MainDataForm

    def get_initial(self):
        user = self.request.user
        person_data = MainPersonData.objects.filter(person=user)
        if person_data.exists():
            return person_data.values().first()
        return super().get_initial()

    def post(self, request, *args, **kwargs):
        form = MainDataForm(data=request.POST)
        if form.is_valid():
            user = self.request.user
            form_data = form.cleaned_data
            person_data = MainPersonData.objects.filter(person=user)
            if person_data.exists():
                person_data = person_data.first()
                person_data.name = form_data.get('name')
                person_data.age = form_data.get('age')
                person_data.sex = form_data.get('sex')
                person_data.height = form_data.get('height')
                person_data.weight = form_data.get('weight')
                person_data.save()
            else:
                MainPersonData.objects.create(
                    person=user,
                    name=form_data.get('name'),
                    age=form_data.get('age'),
                    sex=form_data.get('sex'),
                    height=form_data.get('height'),
                    weight=form_data.get('weight')
                )
        return super().post(request, *args, **kwargs)


class MedicalTest(LoginRequiredMixin, TemplateView):
    template_name = 'web/forms/parameter_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medical_procedure = get_object_or_404(MedicalProcedure,
                                              pk=kwargs.get('test_id'))
        context['form'] = generate_form_by_recommendation(
            medical_procedure)
        return context
