from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ALUMNO', 'Alumno'),
        ('DOCENTE', 'Docente'),
        ('TECNICO', 'Técnico'),
        ('ADMIN', 'Administrador'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='ALUMNO')

class Incidencia(models.Model):
    CATEGORY_CHOICES = (
        ('INFRAESTRUCTURA', 'Infraestructura'),
        ('TI', 'TI / Tecnología'),
        ('MOBILIARIO', 'Mobiliario'),
        ('LIMPIEZA', 'Limpieza'),
        ('SEGURIDAD', 'Seguridad'),
        ('ACADEMICA', 'Gestión Académica'),
        ('MATRICULA', 'Secretaría / Matrícula'),
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('URGENT', 'Urgente'),
    )
    STATUS_CHOICES = (
        ('OPEN', 'Abierto'),
        ('IN_PROGRESS', 'En Progreso'),
        ('RESOLVED', 'Resuelto'),
        ('CLOSED', 'Cerrado'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incidencias_creadas')

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class Comentario(models.Model):
    incidencia = models.ForeignKey(Incidencia, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
