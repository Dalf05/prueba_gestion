# Modelos de la base de datos para el proyecto Colegio UNIE
# Aquí definimos las tablas donde guardamos la info (Usuarios, Incidencias y Comentarios)

from django.db import models
from django.contrib.auth.models import AbstractUser

# Extendemos el usuario normal de Django para meterle el campo de 'rol'
class User(AbstractUser):
    # Definimos qué tipos de personas pueden entrar en la app
    TIPOS_USUARIO = (
        ('ALUMNO', 'Alumno'),
        ('DOCENTE', 'Docente'),
        ('TECNICO', 'Técnico'),
        ('ADMIN', 'Administrador'),
    )
    role = models.CharField(max_length=10, choices=TIPOS_USUARIO, default='ALUMNO')

# Este es el modelo principal: el reporte de que algo se ha roto
class Incidencia(models.Model):
    # Opciones para el formulario
    OPCIONES_CATEGORIA = (
        ('INFRAESTRUCTURA', 'Infraestructura'),
        ('TI', 'TI / Tecnología'),
        ('MOBILIARIO', 'Mobiliario'),
        ('LIMPIEZA', 'Limpieza'),
        ('SEGURIDAD', 'Seguridad'),
        ('ACADEMICA', 'Gestión Académica'),
        ('MATRICULA', 'Secretaría / Matrícula'),
    )
    OPCIONES_PRIORIDAD = (
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('URGENT', 'Urgente'),
    )
    OPCIONES_ESTADO = (
        ('OPEN', 'Abierto'),
        ('IN_PROGRESS', 'En Progreso'),
        ('RESOLVED', 'Resuelto'),
        ('CLOSED', 'Cerrado'),
    )

    # Campos de la tabla
    title = models.CharField(max_length=200, verbose_name="Asunto")
    description = models.TextField(verbose_name="Descripción del problema")
    category = models.CharField(max_length=20, choices=OPCIONES_CATEGORIA, verbose_name="Categoría")
    priority = models.CharField(max_length=10, choices=OPCIONES_PRIORIDAD, default='MEDIUM', verbose_name="Prioridad")
    status = models.CharField(max_length=15, choices=OPCIONES_ESTADO, default='OPEN', verbose_name="Estado")
    location = models.CharField(max_length=100, verbose_name="Ubicación (Aula/Planta)")
    
    # Fechas automáticas
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de resolución")
    
    # Quién lo hizo (Relación con la tabla User)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incidencias_creadas')

    def __str__(self):
        # Para que en el admin de Django se vea el título y no un ID feo
        return f"{self.title} - {self.get_status_display()}"

# Si quisiéramos añadir un chat o comentarios a cada incidencia
class Comentario(models.Model):
    incidencia = models.ForeignKey(Incidencia, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Texto del comentario")
    created_at = models.DateTimeField(auto_now_add=True)
