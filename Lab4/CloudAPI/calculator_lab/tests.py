from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Calculation


class CalculationTestCase(TestCase):

    def setUp(self):
        # This method will run before any test case.
        self.client = APIClient()
        self.calculate_url = '/api/calculate/'

    def test_create_calculation(self):
        # Payload for the test
        payload = {
            "expression": "'2 + 3'"
        }

        # Send a POST request to the calculate endpoint
        response = self.client.post(self.calculate_url, payload, format='json')

        # Check that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the response data contains the correct result
        self.assertEqual(response.data['result'], 5.0)

        # Check that a new calculation record was created
        self.assertEqual(Calculation.objects.count(), 1)
        self.assertEqual(Calculation.objects.get().expression, "'2 + 3'")

    def test_invalid_expression(self):
        # Payload for the test with invalid expression
        payload = {
            "expression": "'2 / 0'"  # This will raise an error
        }

        # Send a POST request to the calculate endpoint
        response = self.client.post(self.calculate_url, payload, format='json')

        # Check that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that no new calculation record was created
        self.assertEqual(Calculation.objects.count(), 0)
