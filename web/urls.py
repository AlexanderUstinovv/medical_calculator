from django.urls import path

from .views import MainView, MainDataView, MedicalTest

urlpatterns = [
    path(r'main/', MainView.as_view(), name='main'),
    path(r'main-data/', MainDataView.as_view(), name='main-data'),
    path(r'medical-test/<int:test_id>/', MedicalTest.as_view(), name='medical-test')
]
