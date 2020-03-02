from django.urls import path

from .views import MainPersonDataRudView, BodyMassDataView

urlpatterns = [
    path(r'maindata/', MainPersonDataRudView.as_view(), name='main-data'),
    path(r'massindex/', BodyMassDataView.as_view(), name='mass-index-get')
]
