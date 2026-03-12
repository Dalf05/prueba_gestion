from django.contrib import admin
from .models import Incident, Comment

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority', 'category')

admin.site.register(Comment)
