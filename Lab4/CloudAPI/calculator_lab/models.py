# calculator_lab/models.py
from django.db import models


'''
Model to store calculator operations with an expression, its result, 
and a timestamp for when the calculation was performed.
'''
class Calculation(models.Model):
    expression = models.CharField(max_length=255)
    result = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
