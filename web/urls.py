from django.urls import path

from .views import MainView, MainDataView

urlpatterns = [
    path(r'main/', MainView.as_view(), name='main'),
    path(r'main-data/', MainDataView.as_view(), name='main-data')
]
