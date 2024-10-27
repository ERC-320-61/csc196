from rest_framework import serializers
from calculator_lab.models import Calculation


class CalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        fields = ['id', 'expression', 'result', 'created_at']