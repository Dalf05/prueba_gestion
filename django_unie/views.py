# Vistas de la aplicación de Gestión de Incidencias - UNIE
# Este archivo controla toda la lógica de lo que el usuario ve en pantalla.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Incidencia, Comentario

# Estas funciones sirven para saber si el usuario es jefe o técnico
def es_administrador(user):
    return user.role == 'ADMIN'

def es_equipo_soporte(user):
    return user.role == 'TECNICO' or user.role == 'ADMIN'

@login_required
def dashboard(request):
    # Si eres alumno, no pintas nada viendo estadísticas, así que te mando a la lista
    if request.user.role == 'ALUMNO':
        return redirect('incidents_list')
    
    # Aquí decidimos qué incidencias puede ver cada uno según su puesto
    if request.user.role in ['ADMIN', 'TECNICO']:
        los_reportes = Incidencia.objects.all()
    elif request.user.role == 'DOCENTE':
        # Los profes solo ven cosas de su ámbito
        categorias_profe = ['TI', 'MOBILIARIO', 'INFRAESTRUCTURA', 'ACADEMICA']
        los_reportes = Incidencia.objects.filter(category__in=categorias_profe)
    else:
        los_reportes = Incidencia.objects.none()
    
    # Calculamos los numeritos del panel (KPIs)
    cantidad_total = los_reportes.count()
    pendientes = los_reportes.filter(status__in=['OPEN', 'IN_PROGRESS']).count()
    resueltas_qs = los_reportes.filter(status__in=['RESOLVED', 'CLOSED'])
    cantidad_resueltas = resueltas_qs.count()
    
    # Calcular cuánto tardamos de media en arreglar cosas
    tiempo_medio_arreglo = 0
    if cantidad_resueltas > 0:
        suma_tiempos = 0
        from django.utils import timezone
        for item in resueltas_qs:
            if item.resolved_at:
                diferencia = item.resolved_at - item.created_at
                suma_tiempos += diferencia.total_seconds() / 3600
        tiempo_medio_arreglo = round(suma_tiempos / cantidad_resueltas, 1) if cantidad_resueltas > 0 else 0
        
    # El cumplimiento SLA es un porcentaje de lo que hemos terminado
    cumplimiento_sla = 0
    if cantidad_total > 0:
        cumplimiento_sla = round((cantidad_resueltas / cantidad_total) * 100)
        
    # Preparamos los datos para que el gráfico de la web funcione (formato JSON)
    from django.db.models import Count
    import json
    conteo_por_categoria = los_reportes.values('category').annotate(total=Count('id'))
    datos_para_grafico = [
        {'label': dict(Incidencia.CATEGORY_CHOICES).get(item['category'], item['category']), 'value': item['total']}
        for item in conteo_por_categoria
    ]
    
    # Mandamos todo al documento HTML (dashboard.html)
    info_para_web = {
        'total_count': cantidad_total,
        'open_count': pendientes,
        'resolved_count': cantidad_resueltas,
        'avg_res_time': tiempo_medio_arreglo,
        'sla_compliance': cumplimiento_sla,
        'recent_incidents': los_reportes.order_by('-created_at')[:5],
        'chart_data_json': json.dumps(datos_para_grafico),
        'role': request.user.role
    }
    return render(request, 'dashboard.html', info_para_web)

@login_required
def incidents_list(request):
    usuario_actual = request.user
    
    # Lógica de filtrado: cada uno ve lo que le toca
    if usuario_actual.role in ['ADMIN', 'TECNICO']:
        listado_completo = Incidencia.objects.all()
    elif usuario_actual.role == 'DOCENTE':
        categorias = ['TI', 'MOBILIARIO', 'INFRAESTRUCTURA', 'ACADEMICA']
        listado_completo = Incidencia.objects.filter(category__in=categorias)
    elif usuario_actual.role == 'ALUMNO':
        categorias = ['LIMPIEZA', 'MOBILIARIO', 'ACADEMICA', 'MATRICULA']
        listado_completo = Incidencia.objects.filter(category__in=categorias)
    else:
        listado_completo = Incidencia.objects.none()
    
    # Si eres jefe o técnico ves el histórico, si no, solo lo que está abierto
    if usuario_actual.role in ['ADMIN', 'TECNICO']:
        las_incidencias = listado_completo.order_by('-created_at')
    else:
        las_incidencias = listado_completo.exclude(status__in=['RESOLVED', 'CLOSED']).order_by('-created_at')
        
    return render(request, 'incidents.html', {'incidencias': las_incidencias})

@login_required
def create_incident(request):
    # Un técnico no debería estar creando incidencias, él está para arreglarlas
    if request.user.role == 'TECNICO':
        return redirect('dashboard')
        
    if request.method == 'POST':
        el_titulo = request.POST.get('title')
        la_descripcion = request.POST.get('description')
        
        # Aquí usamos la función que analiza el texto para ver si es urgente o no
        la_prioridad = analizar_urgencia(el_titulo, la_descripcion)
        
        nueva_incidencia = Incidencia.objects.create(
            title=el_titulo,
            description=la_descripcion,
            category=request.POST.get('category'),
            location=request.POST.get('location'),
            priority=la_prioridad,
            created_by=request.user
        )
        messages.success(request, f'La incidencia "{el_titulo}" se ha guardado bien. Prioridad calculada: {nueva_incidencia.get_priority_display()}.')
        return redirect('incidents_list')
    return render(request, 'create_incident.html')

@login_required
@user_passes_test(es_administrador)
def settings_view(request):
    from .models import User
    # Listamos a los demás usuarios del sistema para gestión
    otros_usuarios = User.objects.exclude(pk=request.user.pk)
    # Sacamos las sitios que ya existen en la base de datos
    sitios_registrados = Incidencia.objects.values_list('location', flat=True).distinct()
    return render(request, 'settings.html', {'system_users': otros_usuarios, 'locations': sitios_registrados})

def analizar_urgencia(titulo, descripcion):
    """
    Esta función mira si hay palabras 'chungas' en el reporte para ponerle prioridad alta.
    Es un filtro de texto sencillo.
    """
    todo_el_texto = (titulo + " " + descripcion).lower()
    
    # Si hay peligro real
    palabras_criticas = ['peligro', 'fuego', 'quemado', 'inundación', 'robo', 'emergencia', 'crítico', 'urgente']
    if any(paly in todo_el_texto for paly in palabras_criticas):
        return 'URGENT'
    
    # Si impide dar clase o trabajar
    palabras_importantes = ['no funciona', 'bloqueado', 'roto', 'clase', 'examen', 'parado', 'avería']
    if any(paly in todo_el_texto for paly in palabras_importantes):
        return 'HIGH'
    
    # Si es algo molesto pero se puede esperar
    palabras_medias = ['luz', 'aire', 'sucio', 'ruido', 'bombilla', 'ventana']
    if any(paly in todo_el_texto for paly in palabras_medias):
        return 'MEDIUM'
        
    return 'LOW'

@login_required
def update_status(request, pk):
    el_reporte = get_object_or_404(Incidencia, pk=pk)
    
    # Comprobamos permisos: solo jefes, técnicos o el que lo escribió pueden tocarlo
    if request.user.role not in ['ADMIN', 'TECNICO'] and el_reporte.created_by != request.user:
        messages.error(request, "No puedes tocar una incidencia que no es tuya.")
        return redirect('incidents_list')

    if request.method == 'POST':
        estado_nuevo = request.POST.get('status')
        
        # Un usuario normal solo puede cerrar su reporte, no cambiarlo a 'en proceso' por ejemplo
        if request.user.role not in ['ADMIN', 'TECNICO'] and estado_nuevo != 'CLOSED':
            messages.error(request, "Solo el equipo de soporte puede cambiar estados intermedios.")
            return redirect('incidents_list')
            
        el_reporte.status = estado_nuevo
        
        # Guardamos cuándo se cerró para luego sacar las estadísticas
        if estado_nuevo in ['RESOLVED', 'CLOSED'] and not el_reporte.resolved_at:
            from django.utils import timezone
            el_reporte.resolved_at = timezone.now()
            
        el_reporte.save()
        messages.success(request, f'Se ha actualizado el reporte #{el_reporte.id} correctamente.')
        
    return redirect('incidents_list')
