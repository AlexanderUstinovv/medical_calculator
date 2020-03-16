from django.contrib.auth.models import User

from body_mass_calculator.models import MainPersonData

from medical_test.cardiovascular_risk import PersonalData
from medical_test.models import MedicalProcedureResult, ParameterValue
from medical_test.cardiovascular_risk import calculate_risk

LOW_PERCENT = 1
HIGH_PERCENT = 10
MEDIUM_PERCENT = 5

CHOLESTEROL_RESEARCH_ID = 5
CHOLESTEROL_PARAMETER_ID = 12
ARTERIAL_PRESSURE_RESEARCH_ID = 3
SYSTOLIC_PRESSURE_PARAMETER_ID = 9

MAIN_DATA_REQUIRED = 'Для получения статуса ' \
                     'необходимо заполнить данные о себе'

LOW_RISK_STATUS_MESSAGE = 'Низкий риск получения ' \
                          'сердечно-сосудистого заболевания'

MEDIUM_RISK_STATUS_MESSAGE = 'Средний риск получения ' \
                             'сердечно-сосудистого заболевания'

HIGH_RISK_STATUS_MESSAGE = 'Высокий риск получения ' \
                           'сердечно-сосудистого заболевания'

HIGHEST_RISK_STATUS_MESSAGE = 'Очень высокий риск получения ' \
                              'сердечно-сосудистого заболевания'

ADDITIONAL_DATA_REQUIRED = 'Для получения статуса необходимо ' \
                           'заполнить данные об артериальном ' \
                           'давлении и уровне холлестерина'


def get_parameter_value(user: User,
                        research_id: int,
                        parameter_id: int) -> float:
    research = MedicalProcedureResult.objects.filter(
        user=user,
        medical_procedure__pk=research_id
    )
    if research.exists():
        parameter_value = ParameterValue.objects.filter(
            medical_procedure_result=research.first(),
            parameter__pk=parameter_id
        )
        if parameter_value.exists():
            return float(parameter_value.first().value)
    raise ValueError('Not found data for current user')


def get_risk_message(percent: int) -> str:
    if percent < LOW_PERCENT:
        return LOW_RISK_STATUS_MESSAGE
    elif LOW_PERCENT <= percent < MEDIUM_PERCENT:
        return MEDIUM_RISK_STATUS_MESSAGE
    elif MEDIUM_PERCENT <= percent < HIGH_PERCENT:
        return HIGH_RISK_STATUS_MESSAGE
    elif percent > HIGH_PERCENT:
        return HIGHEST_RISK_STATUS_MESSAGE
    else:
        return LOW_RISK_STATUS_MESSAGE


def get_risk_status(user: User) -> str:
    data = MainPersonData.objects.filter(person=user)
    if not data.exists():
        return MAIN_DATA_REQUIRED

    MedicalProcedureResult.objects.filter()

    try:
        cholesterol = get_parameter_value(user,
                                          CHOLESTEROL_RESEARCH_ID,
                                          CHOLESTEROL_PARAMETER_ID)
        pressure = get_parameter_value(user,
                                       ARTERIAL_PRESSURE_RESEARCH_ID,
                                       SYSTOLIC_PRESSURE_PARAMETER_ID)
        data = data.first()
        person_data = PersonalData(
            sex=data.sex,
            age=data.age,
            smoking=data.smoking,
            cholesterol=cholesterol,
            systolic_pressure=pressure
        )

        risk_status = calculate_risk(person_data)
        return get_risk_message(risk_status)

    except ValueError:
        return ADDITIONAL_DATA_REQUIRED
