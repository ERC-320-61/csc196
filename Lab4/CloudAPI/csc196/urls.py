#csc196/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include("apis.urls")),
    path('', RedirectView.as_view(url='/api/', permanent=True)),
]
