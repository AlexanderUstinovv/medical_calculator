from body_mass_calculator.models import MainPersonData, BodyMassIndex
from rest_framework import serializers


class MainPersonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPersonData
        fields = ['person', 'name', 'sex', 'age', 'height', 'weight']
        read_only_fields = ['person']

    def validate_name(self, value):
        if len(value) > 15:
            raise serializers.ValidationError('Name length must be lower 16 symbols')
        return value

    def validate_sex(self, value):
        if value not in (MainPersonData.MALE, MainPersonData.FEMALE):
            raise serializers.ValidationError('Sex must be M of F')
        return value

    def validate_age(self, value):
        if value < 21:
            raise serializers.ValidationError('Age must be greater or equal 21')
        return value

    def validate_height(self, value):
        if value < 0:
            raise serializers.ValidationError('Height must be positive')
        if value > 300:
            raise serializers.ValidationError('Too much height')
        return value

    def validate_weight(self, value):
        if value < 0:
            raise serializers.ValidationError('Weight must be positive')
        if value > 1000:
            raise serializers.ValidationError('Too much weight')
        return value


class BodyMassIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyMassIndex
        serializer_class = ['person', 'value']
        fields = ['person', 'value']


class ParameterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    measurement = serializers.CharField(max_length=10)


class RecommendationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    parameters = serializers.ListField(child=ParameterSerializer())


class RecommendationsSerializer(serializers.Serializer):
    recommendations = serializers.ListField(child=RecommendationSerializer())


class UserParameterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    value = serializers.FloatField()


class UserMedicalProcedureSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parameters = serializers.ListField(child=UserParameterSerializer())


class UserMedicalProceduresSerializer(serializers.Serializer):
    procedures = serializers.ListField(child=UserMedicalProcedureSerializer())
