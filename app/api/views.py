from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from body_mass_calculator.models import MainPersonData, BodyMassIndex
from medical_test.recommendations import recommend_medical_test

from medical_test.models import MedicalProcedure
from medical_test.models import Parameter, MedicalProcedureResult
from medical_test.models import ParameterValue

from .serializers import MainPersonDataSerializer
from .serializers import BodyMassIndexSerializer
from .serializers import RecommendationsSerializer
from .serializers import UserMedicalProceduresSerializer

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

    @swagger_auto_schema(responses={200: RecommendationsSerializer(many=True)})
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


def get_or_create_procedure_result(procedure_id: int, user):
    med_proc = MedicalProcedure.objects.get(id=procedure_id)
    medical_result = MedicalProcedureResult.objects.filter(
        medical_procedure=med_proc,
        user=user
    )
    if medical_result.exists():
        return medical_result.first()
    return MedicalProcedureResult.objects.create(
        medical_procedure=MedicalProcedure.objects.get(id=procedure_id),
        user=user,
        value=0
    )


def update_or_create_parameter(procedure_result: MedicalProcedureResult,
                               parameter_id: int,
                               value: float):
    parameter_value = ParameterValue.objects.filter(
        medical_procedure_result=procedure_result,
        parameter__pk=parameter_id
    )

    if parameter_value.exists():
        parameter_value.update(value=value)
    else:
        ParameterValue.objects.create(
            medical_procedure_result=procedure_result,
            parameter=Parameter.objects.get(id=parameter_id),
            value=value
        )


class RecommendationParameterValues(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={201: UserMedicalProceduresSerializer(many=True)})
    def post(self, request):
        user = self.request.user
        serializer = UserMedicalProceduresSerializer(
            data=request.data)
        if serializer.is_valid():
            data = dict(serializer.validated_data)
            valid_data = [dict(item) for item in data.get('procedures', [])]
            for item in valid_data:
                procedure = get_or_create_procedure_result(item.get('id'), user)
                for param in item.get('parameters'):
                    param = dict(param)
                    update_or_create_parameter(
                        procedure,
                        param.get('id'),
                        param.get('value')
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
