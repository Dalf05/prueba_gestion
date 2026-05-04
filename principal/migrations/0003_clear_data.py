from django.db import migrations

def clear_incidents(apps, schema_editor):
    Incidencia = apps.get_model('principal', 'Incidencia')
    Incidencia.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('principal', '0002_seed_users'), 
    ]

    operations = [
        migrations.RunPython(clear_incidents),
    ]
