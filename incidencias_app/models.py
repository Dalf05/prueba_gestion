from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    PRIORITIES = (
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    )
    STATUSES = (
        ('open', 'Abierto'),
        ('in_progress', 'En Progreso'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
    )
    CATEGORIES = (
        ('Infraestructura', 'Infraestructura'),
        ('TI', 'TI / Tecnología'),
        ('Mobiliario', 'Mobiliario'),
        ('Limpieza', 'Limpieza'),
        ('Seguridad', 'Seguridad'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORIES)
    priority = models.CharField(max_length=10, choices=PRIORITIES, default='medium')
    status = models.CharField(max_length=20, choices=STATUSES, default='open')
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incidents', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

class Comment(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario en {self.incident.title}"
