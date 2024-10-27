# apis/urls.py
from django.urls import path# apis/urls.py
from django.urls import path
from .views import CalculationViewSet, home

urlpatterns = [
    path('calculator/', CalculationViewSet.as_view({'post': 'create'}), name="calculator"),
    # Adjust according to your API
    path('', home, name='home'),
]
