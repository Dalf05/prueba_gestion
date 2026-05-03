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
    
    # Tiempo medio de resolución (calculado si hay datos)
    avg_res_time = 0
    if resolved_count > 0:
        total_time = 0
        from django.utils import timezone
        for inc in resolved_qs:
            if inc.resolved_at:
                diff = inc.resolved_at - inc.created_at
                total_time += diff.total_seconds() / 3600
        avg_res_time = round(total_time / resolved_count, 1) if resolved_count > 0 else 0
        
    # Cumplimiento SLA (ejemplo de cálculo real: % resueltas sobre totales)
    sla_compliance = 0
    if total_count > 0:
        sla_compliance = round((resolved_count / total_count) * 100)
        
    # Datos para el gráfico de distribución por categoría
    from django.db.models import Count
    import json
    category_counts = queryset.values('category').annotate(count=Count('id'))
    chart_data = [
        {'label': dict(Incidencia.CATEGORY_CHOICES).get(item['category'], item['category']), 'value': item['count']}
        for item in category_counts
    ]
    
    context = {
        'total_count': total_count,
        'open_count': open_count,
        'resolved_count': resolved_count,
        'avg_res_time': avg_res_time,
        'sla_compliance': sla_compliance,
        'recent_incidents': queryset.order_by('-created_at')[:5],
        'chart_data_json': json.dumps(chart_data),
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
    from .models import User
    users = User.objects.exclude(pk=request.user.pk)
    # Por ahora las ubicaciones son un conjunto de las usadas en incidencias reales
    locations = Incidencia.objects.values_list('location', flat=True).distinct()
    return render(request, 'settings.html', {'system_users': users, 'locations': locations})

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
def update_status(request, pk):
    incidencia = get_object_or_404(Incidencia, pk=pk)
    
    # Solo el Admin, el Técnico o el propio creador pueden modificar el estado
    if request.user.role not in ['ADMIN', 'TECNICO'] and incidencia.created_by != request.user:
        messages.error(request, "No tienes permiso para modificar esta incidencia.")
        return redirect('incidents_list')

    if request.method == 'POST':
        nuevo_estado = request.POST.get('status')
        
        # Si no es admin/tecnico, solo puede cambiar a CLOSED
        if request.user.role not in ['ADMIN', 'TECNICO'] and nuevo_estado != 'CLOSED':
            messages.error(request, "Solo puedes cerrar tus propias incidencias.")
            return redirect('incidents_list')
            
        incidencia.status = nuevo_estado
        
        # Si se marca como resuelto o cerrado, guardamos la fecha
        if nuevo_estado in ['RESOLVED', 'CLOSED'] and not incidencia.resolved_at:
            from django.utils import timezone
            incidencia.resolved_at = timezone.now()
            
        incidencia.save()
        messages.success(request, f'Estado de la incidencia #{incidencia.id} actualizado a {incidencia.get_status_display()}.')
        
    return redirect('incidents_list')
