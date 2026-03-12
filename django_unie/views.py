from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Incidencia, Comentario

# Funciones de comprobación de roles para decoradores
def is_admin(user):
    return user.role == 'ADMIN'

def is_tecnico(user):
    return user.role == 'TECNICO' or user.role == 'ADMIN'

@login_required
def dashboard(request):
    # Los alumnos no ven el dashboard de estadísticas, solo el listado
    if request.user.role == 'ALUMNO':
        return redirect('incidents_list')
    
    # Filtrado de incidencias según rol
    if request.user.role in ['ADMIN', 'TECNICO']:
        queryset = Incidencia.objects.all()
    elif request.user.role == 'DOCENTE':
        categories = ['TI', 'MOBILIARIO', 'INFRAESTRUCTURA', 'ACADEMICA']
        queryset = Incidencia.objects.filter(category__in=categories)
    else:
        queryset = Incidencia.objects.none()
    
    # CÁLCULO DE KPIs PARA EL PANEL
    total_count = queryset.count()
    open_count = queryset.filter(status__in=['OPEN', 'IN_PROGRESS']).count()
    resolved_qs = queryset.filter(status__in=['RESOLVED', 'CLOSED'])
    resolved_count = resolved_qs.count()
    
    # Tiempo medio de resolución (simulado o calculado si hay datos)
    avg_res_time = 0
    if resolved_count > 0:
        avg_res_time = 14 # Valor de ejemplo en horas
        
    context = {
        'total_count': total_count,
        'open_count': open_count,
        'resolved_count': resolved_count,
        'avg_res_time': avg_res_time,
        'sla_compliance': 94, # % de ejemplo
        'role': request.user.role
    }
    return render(request, 'dashboard.html', context)

@login_required
def incidents_list(request):
    user = request.user
    # Filtramos por categorías según rol
    if user.role in ['ADMIN', 'TECNICO']:
        queryset = Incidencia.objects.all()
    elif user.role == 'DOCENTE':
        categories = ['TI', 'MOBILIARIO', 'INFRAESTRUCTURA', 'ACADEMICA']
        queryset = Incidencia.objects.filter(category__in=categories)
    elif user.role == 'ALUMNO':
        categories = ['LIMPIEZA', 'MOBILIARIO', 'ACADEMICA', 'MATRICULA']
        queryset = Incidencia.objects.filter(category__in=categories)
    else:
        queryset = Incidencia.objects.none()
    
    # Para el Admin y Técnico, mostramos TODO en el registro central por defecto
    # Para otros, solo las activas
    if user.role in ['ADMIN', 'TECNICO']:
        incidencias = queryset.order_by('-created_at')
    else:
        incidencias = queryset.exclude(status__in=['RESOLVED', 'CLOSED']).order_by('-created_at')
        
    return render(request, 'incidents.html', {'incidencias': incidencias})

@login_required
def create_incident(request):
    if request.user.role == 'TECNICO':
        return redirect('dashboard') # Los técnicos no crean, solo resuelven
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # SCRIPT DE ANÁLISIS AUTOMÁTICO DE PRIORIDAD
        priority = analyze_priority_logic(title, description)
        
        incidencia = Incidencia.objects.create(
            title=title,
            description=description,
            category=request.POST.get('category'),
            location=request.POST.get('location'),
            priority=priority,
            created_by=request.user
        )
        messages.success(request, f'Incidencia "{title}" registrada correctamente con prioridad {incidencia.get_priority_display()}.')
        return redirect('incidents_list')
    return render(request, 'create_incident.html')

@login_required
@user_passes_test(is_admin)
def settings_view(request):
    locations = ['Edificio A', 'Edificio B', 'Laboratorios', 'Biblioteca', 'Cafetería', 'Zonas Deportivas']
    return render(request, 'settings.html', {'locations': locations})

def analyze_priority_logic(title, description):
    """
    Script de segmentación automática de prioridad.
    Analiza palabras clave para determinar la urgencia.
    """
    text = (title + " " + description).lower()
    
    # Prioridad URGENTE: Peligro, rotura crítica, seguridad
    if any(word in text for word in ['peligro', 'fuego', 'inundación', 'robo', 'emergencia', 'crítico']):
        return 'URGENT'
    
    # Prioridad ALTA: Bloqueo de clases o administración
    if any(word in text for word in ['no funciona', 'bloqueado', 'roto', 'clase', 'examen']):
        return 'HIGH'
    
    # Prioridad MEDIA: Funcionamiento parcial o incomodidad
    if any(word in text for word in ['luz', 'aire', 'sucio', 'ruido']):
        return 'MEDIUM'
        
    return 'LOW'

@login_required
@user_passes_test(is_tecnico)
def update_status(request, pk):
    incidencia = get_object_or_404(Incidencia, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('status')
        incidencia.status = nuevo_estado
        
        # Si se marca como resuelto, guardamos la fecha
        if nuevo_estado in ['RESOLVED', 'CLOSED'] and not incidencia.resolved_at:
            from django.utils import timezone
            incidencia.resolved_at = timezone.now()
            
        incidencia.save()
    return redirect('incidents_list')
