from django.db import migrations
from django.contrib.auth.hashers import make_password

def seed_users(apps, schema_editor):
    User = apps.get_model('django_unie', 'User')
    
    # Datos de los usuarios iniciales
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@unie.com',
            'password': make_password('unie2026'),
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'docente',
            'email': 'docente@unie.com',
            'password': make_password('unie2026'),
            'role': 'DOCENTE',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'tecnico',
            'email': 'tecnico@unie.com',
            'password': make_password('unie2026'),
            'role': 'TECNICO',
            'is_staff': False,
            'is_superuser': False
        },
        {
            'username': 'alumno',
            'email': 'alumno@unie.com',
            'password': make_password('unie2026'),
            'role': 'ALUMNO',
            'is_staff': False,
            'is_superuser': False
        }
    ]
    
    for data in users_data:
        User.objects.create(**data)

    # Crear incidencias iniciales
    Incidencia = apps.get_model('django_unie', 'Incidencia')
    admin_user = User.objects.get(username='admin')
    docente_user = User.objects.get(username='docente')
    alumno_user = User.objects.get(username='alumno')
    tecnico_user = User.objects.get(username='tecnico')

    incidencias_data = [
        {
            'title': 'Fallo proyector Epson Aula 203',
            'description': 'El proyector muestra una dominante amarilla y parpadea cada pocos minutos. Se ha probado con varios cables HDMI y el problema persiste.',
            'category': 'TI',
            'priority': 'HIGH',
            'status': 'IN_PROGRESS',
            'location': 'Edificio Principal - Planta 2',
            'created_by': docente_user
        },
        {
            'title': 'Filtración techo pasillo Biblioteca',
            'description': 'Gotera activa tras las lluvias de anoche. Hay riesgo de que el agua llegue a las estanterías de la sección de Humanidades.',
            'category': 'INFRAESTRUCTURA',
            'priority': 'URGENT',
            'status': 'OPEN',
            'location': 'Edificio Biblioteca - Planta 1',
            'created_by': admin_user
        },
        {
            'title': 'Silla ergonómica dañada Lab 05',
            'description': 'El pistón hidráulico no mantiene la altura. El alumno no puede trabajar cómodamente.',
            'category': 'MOBILIARIO',
            'priority': 'LOW',
            'status': 'RESOLVED',
            'location': 'Laboratorios - Planta Baja',
            'created_by': alumno_user
        },
        {
            'title': 'Problemas acceso Wi-Fi Campus-Guest',
            'description': 'Varios alumnos reportan que la red de invitados no redirige al portal cautivo en la zona de la cafetería.',
            'category': 'TI',
            'priority': 'MEDIUM',
            'status': 'OPEN',
            'location': 'Cafetería / Zonas Comunes',
            'created_by': alumno_user
        },
        {
            'title': 'Cierre defectuoso puerta Aula 101',
            'description': 'La cerradura electrónica se queda bloqueada intermitentemente. Esta mañana hubo que avisar a seguridad para entrar.',
            'category': 'SEGURIDAD',
            'priority': 'HIGH',
            'status': 'IN_PROGRESS',
            'location': 'Edificio A - Planta 1',
            'created_by': docente_user
        },
        {
            'title': 'Error en actas de evaluación trimestral',
            'description': 'El desplegable de notas no carga para el grupo M2-B. Se ha intentado recargar la página pero da error 500.',
            'category': 'ACADEMICA',
            'priority': 'HIGH',
            'status': 'OPEN',
            'location': 'Secretaría Virtual',
            'created_by': docente_user
        },
        {
            'title': 'Jabón agotado aseos Planta 0',
            'description': 'Los dispensadores de los baños masculinos de la entrada están vacíos desde el viernes.',
            'category': 'LIMPIEZA',
            'priority': 'LOW',
            'status': 'OPEN',
            'location': 'Edificio Principal - Planta Baja',
            'created_by': alumno_user
        }
    ]

    for inc in incidencias_data:
        Incidencia.objects.create(**inc)

class Migration(migrations.Migration):

    dependencies = [
        ('django_unie', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_users),
    ]
