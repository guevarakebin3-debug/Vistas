"""
URL configuration for Djangoproyecto project.
"""
from django.contrib import admin
from django.urls import path, include
from empleados import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('empleados.urls')),
]
