# apis/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from calculator_lab.services import calculate
from django.http import HttpResponse

''' HOME '''


def home(request):
    return HttpResponse("Welcome to the Calculator API")


class CalculationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        if not all(key in data for key in ('num1', 'num2', 'operation')):
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

        num1 = data['num1']
        num2 = data['num2']
        operation = data['operation']

        result, error = calculate(num1, num2, operation)
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"result": result}, status=status.HTTP_200_OK)
