from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Incidencia, Comentario

# Funciones de comprobación de roles para los decoradores
# Esto lo he sacado de un tutorial para que solo el admin entre en algunas partes
def is_admin(user):
    return user.role == 'ADMIN'

def is_tecnico(user):
    return user.role == 'TECNICO' or user.role == 'ADMIN'

@login_required
def dashboard(request):
    # Los alumnos no ven el dashboard de estadísticas, segun me han pedido los que lo usan
    if request.user.role == 'ALUMNO':
        return redirect('incidents_list')
    
    # Miramos que incidencias puede ver cada uno dependiendo del rol
    if request.user.role in ['ADMIN', 'TECNICO']:
        queryset = Incidencia.objects.all()
    elif request.user.role == 'DOCENTE':
        categories = ['TI', 'MOBILIARIO', 'INFRAESTRUCTURA', 'ACADEMICA']
        queryset = Incidencia.objects.filter(category__in=categories)
    else:
        queryset = Incidencia.objects.none() # Por si acaso, que no vea nada
    
    # CÁLCULOS PARA EL PANEL (KPIs)
    total_count = queryset.count()
    open_count = queryset.filter(status__in=['OPEN', 'IN_PROGRESS']).count()
    resolved_qs = queryset.filter(status__in=['RESOLVED', 'CLOSED'])
    resolved_count = resolved_qs.count()
    
    # Tiempo medio de resolución (hecho a mano con un bucle)
    avg_res_time = 0
    if resolved_count > 0:
        total_time = 0
        from django.utils import timezone
        for inc in resolved_qs:
            if inc.resolved_at:
                diff = inc.resolved_at - inc.created_at
                total_time += diff.total_seconds() / 3600 # Lo pasamos a horas
        avg_res_time = round(total_time / resolved_count, 1) if resolved_count > 0 else 0
        
    # Cumplimiento SLA (basico, porcentaje de resueltas)
    sla_compliance = 0
    if total_count > 0:
        sla_compliance = round((resolved_count / total_count) * 100)
        
    # Esto es para el grafico de circulo, pasamos los datos a json
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
    # Aqui tambien filtramos segun quien sea el que mira la lista
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
    
    # Si eres admin o tecnico ves todo, si no solo lo que no esta resuelto todavia
    if user.role in ['ADMIN', 'TECNICO']:
        incidencias = queryset.order_by('-created_at')
    else:
        incidencias = queryset.exclude(status__in=['RESOLVED', 'CLOSED']).order_by('-created_at')
        
    return render(request, 'incidents.html', {'incidencias': incidencias})

@login_required
def create_incident(request):
    # Los tecnicos no pueden crear incidencias, no tendria sentido
    if request.user.role == 'TECNICO':
        return redirect('dashboard')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Funcion que calcula la prioridad automaticamente
        priority = calcular_prioridad(title, description)
        
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
    # Solo para el administrador, para resetear cosas o ver usuarios
    from .models import User
    users = User.objects.exclude(pk=request.user.pk)
    locations = Incidencia.objects.values_list('location', flat=True).distinct()
    return render(request, 'settings.html', {'system_users': users, 'locations': locations})

def calcular_prioridad(title, description):
    """
    Funcion para ver si una incidencia es urgente o no.
    He puesto unas palabras clave para que decida solo.
    """
    text = (title + " " + description).lower()
    
    # URGENTE: si hay fuego, robos o cosas graves de seguridad
    if any(word in text for word in ['peligro', 'fuego', 'inundación', 'robo', 'emergencia', 'crítico']):
        return 'URGENT'
    
    # ALTA: cosas que impiden dar clase normal
    if any(word in text for word in ['no funciona', 'bloqueado', 'roto', 'clase', 'examen']):
        return 'HIGH'
    
    # MEDIA: casi todo lo demas por defecto si no es urgente
    if any(word in text for word in ['luz', 'aire', 'sucio', 'ruido']):
        return 'MEDIUM'
        
    return 'LOW'

@login_required
def update_status(request, pk):
    # Aqui cambiamos el estado de la incidencia (de abierto a resuelto, por ejemplo)
    incidencia = get_object_or_404(Incidencia, pk=pk)
    
    # Solo el que la creo o los jefes pueden tocar esto
    if request.user.role not in ['ADMIN', 'TECNICO'] and incidencia.created_by != request.user:
        messages.error(request, "No tienes permiso para modificar esta incidencia.")
        return redirect('incidents_list')

    if request.method == 'POST':
        nuevo_estado = request.POST.get('status')
        
        # Si eres alumno solo puedes cerrarla tu mismo si ya esta resuelta por admin
        if request.user.role not in ['ADMIN', 'TECNICO'] and nuevo_estado != 'CLOSED':
            messages.error(request, "Solo puedes cerrar tus propias incidencias.")
            return redirect('incidents_list')
            
        incidencia.status = nuevo_estado
        
        # Guardamos cuando se resolvio
        if nuevo_estado in ['RESOLVED', 'CLOSED'] and not incidencia.resolved_at:
            from django.utils import timezone
            incidencia.resolved_at = timezone.now()
            
        incidencia.save()
        messages.success(request, f'Estado de la incidencia #{incidencia.id} actualizado a {incidencia.get_status_display()}.')
        
    return redirect('incidents_list')
