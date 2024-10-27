from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CalculationViewSet, calculate

router = DefaultRouter()
router.register(r'calculations', CalculationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/calculate/', calculate, name='calculate'),
]
