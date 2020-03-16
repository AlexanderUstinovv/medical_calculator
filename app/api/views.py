from body_mass_calculator.models import MainPersonData, BodyMassIndex
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import MainPersonDataSerializer, BodyMassIndexSerializer


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
