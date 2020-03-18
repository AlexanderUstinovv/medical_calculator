from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from body_mass_calculator.models import MainPersonData, BodyMassIndex
from medical_test.recommendations import recommend_medical_test

from medical_test.models import Parameter

from .serializers import MainPersonDataSerializer
from .serializers import BodyMassIndexSerializer
from .serializers import RecommendationsSerializer

from .request_object.recommendation import Parameter as ResponseParameter
from .request_object.recommendation import Recommendations
from .request_object.recommendation import Recommendation


class MainPersonDataRudView(generics.mixins.CreateModelMixin,
                            generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MainPersonDataSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return MainPersonData.objects.all()

    def get_object(self):
        user = self.request.user
        return MainPersonData.objects.get(person=user)

    def perform_create(self, serializer):
        serializer.save(person=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data['person'] = self.request.user.id
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data['person'] = self.request.user.id
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class BodyMassDataView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BodyMassIndexSerializer

    def get_queryset(self):
        return BodyMassIndex.objects.all()

    def get_object(self):
        user = self.request.user
        return BodyMassIndex.objects.get(person=user)


class ListRecommendations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        main_data = MainPersonData.objects.filter(person=user)
        procedures = recommend_medical_test(main_data.first().sex,
                                            main_data.first().age)
        recommendations = []
        for procedure in procedures:
            parameters = Parameter.objects.filter(
                medical_procedure=procedure
            )
            params = [ResponseParameter(item.id,
                                        item.name,
                                        item.measurement.name)
                      for item in parameters]
            recommendations.append(Recommendation(procedure.id,
                                                  procedure.name,
                                                  params))
        recommendations_object = Recommendations(
            recommendations=recommendations)
        serializer = RecommendationsSerializer(recommendations_object)
        return Response(serializer.data)
