from django.urls import path

from .views import main, MainDataView

urlpatterns = [
    path(r'main/', main, name='main'),
    path(r'main-data/', MainDataView.as_view(), name='main-data')
]
