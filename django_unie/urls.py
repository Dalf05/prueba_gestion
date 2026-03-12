from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Vistas de la aplicación
    path('', views.dashboard, name='dashboard'),
    path('incidencias/', views.incidents_list, name='incidents_list'),
    path('incidencias/nueva/', views.create_incident, name='create_incident'),
    path('incidencias/<int:pk>/estado/', views.update_status, name='update_status'),
    path('configuracion/', views.settings_view, name='settings'),
]
