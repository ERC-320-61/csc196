# calculator_lab/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class CalculatorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/calculator/'

    def test_addition(self):
        data = {
            'num1': 10,
            'num2': 5,
            'operation': 'add'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 15.0)

    def test_subtraction(self):
        data = {
            'num1': 10,
            'num2': 5,
            'operation': 'subtract'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 5.0)

    def test_multiplication(self):
        data = {
            'num1': 10,
            'num2': 5,
            'operation': 'multiply'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 50.0)

    def test_division(self):
        data = {
            'num1': 10,
            'num2': 5,
            'operation': 'divide'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 2.0)

    def test_division_by_zero(self):
        data = {
            'num1': 10,
            'num2': 0,
            'operation': 'divide'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Division by zero")

    def test_invalid_operation(self):
        data = {
            'num1': 10,
            'num2': 5,
            'operation': 'invalid'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Unsupported operation")

    def test_invalid_input(self):
        data = {
            'num1': 'a',
            'num2': 5,
            'operation': 'add'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Invalid number format")
