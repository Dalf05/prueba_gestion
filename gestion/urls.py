# Listado de URLs para que el servidor sepa dónde ir
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Pantalla de acceso y salir
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Aquí están las pantallas de la aplicación
    path('', views.dashboard, name='dashboard'), # Página principal
    path('incidencias/', views.incidents_list, name='incidents_list'), # Listado de fallos
    path('incidencias/nueva/', views.create_incident, name='create_incident'), # Formulario de reporte
    path('incidencias/<int:pk>/estado/', views.update_status, name='update_status'), # Para cambiar el estado
    path('configuracion/', views.settings_view, name='settings'), # Ajustes del sistema (Solo Admin)
]
