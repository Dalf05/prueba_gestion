from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rutas para entrar y salir (Login y Logout)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Lo que se ve dentro de la web
    path('', views.dashboard, name='dashboard'), # Pagina principal nada mas entrar
    path('incidencias/', views.incidents_list, name='incidents_list'), # Listado de quejas
    path('incidencias/nueva/', views.create_incident, name='create_incident'), # Formulario para crear una
    path('incidencias/<int:pk>/estado/', views.update_status, name='update_status'), # Para cambiar el estado
    path('configuracion/', views.settings_view, name='settings'), # Ajustes del admin
]
