# Archivo de rutas principal de SISTEMA UNIE
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administración predeterminado de Django
    path('admin/', admin.site.urls),
    # Aquí cargamos todas las rutas de nuestra aplicación de gestión
    path('', include('gestion.urls')),
]
