from django.db import migrations
from django.contrib.auth.hashers import make_password

def seed_users(apps, schema_editor):
    User = apps.get_model('gestion', 'User')
    
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

class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_users),
    ]
