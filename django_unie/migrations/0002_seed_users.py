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

    incidencias_data = [
        {
            'title': 'Fallo proyector Aula 102',
            'description': 'El proyector no recibe señal del HDMI.',
            'category': 'TI',
            'priority': 'HIGH',
            'status': 'OPEN',
            'location': 'Edificio A - Planta 1',
            'created_by': docente_user
        },
        {
            'title': 'Gotera en pasillo biblioteca',
            'description': 'Hay una filtración de agua cerca de la sección de ingeniería.',
            'category': 'INFRAESTRUCTURA',
            'priority': 'URGENT',
            'status': 'IN_PROGRESS',
            'location': 'Biblioteca - Planta 0',
            'created_by': admin_user
        },
        {
            'title': 'Silla rota laboratorio 3',
            'description': 'Una de las sillas ergonómicas tiene la base partida.',
            'category': 'MOBILIARIO',
            'priority': 'LOW',
            'status': 'OPEN',
            'location': 'Laboratorios - Planta 2',
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
