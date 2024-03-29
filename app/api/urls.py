from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

from .views import ListRecommendations
from .views import RecommendationParameterValues
from .views import MainPersonDataRudView, BodyMassDataView

urlpatterns = [
    path(r'token-auth/', obtain_jwt_token, name='token-auth'),
    path(r'token-refresh/', refresh_jwt_token, name='token-refresh'),
    path(r'main-data/', MainPersonDataRudView.as_view(), name='main-data'),
    path(r'mass-index/', BodyMassDataView.as_view(), name='mass-index-get'),
    path(r'recommendations/', ListRecommendations.as_view(), name='recommendations'),
    path(r'medical-results/', RecommendationParameterValues.as_view(), name='medical_result')
]
