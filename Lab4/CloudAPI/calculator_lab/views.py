from django.shortcuts import render

from rest_framework import viewsets
from .models import Calculation
from .serializers import CalculationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import ast


class CalculationViewSet(viewsets.ModelViewSet):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer


@api_view(['POST'])
def calculate(request):
    expression = request.data.get('expression')
    try:
        # Evaluate the expression safely
        result = eval(ast.literal_eval(expression))
        calculation = Calculation.objects.create(expression=expression, result=result)
        serializer = CalculationSerializer(calculation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
