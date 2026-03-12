from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Incident, Comment
from .serializers import IncidentSerializer, CommentSerializer

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all().order_by('-created_at')
    serializer_class = IncidentSerializer

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        incident = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # En un entorno real usaríamos request.user
            serializer.save(incident=incident, user_id=1) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = Incident.objects.count()
        open_count = Incident.objects.filter(status='open').count()
        resolved_count = Incident.objects.filter(status='resolved').count()
        by_category = Incident.objects.values('category').annotate(count=Count('id'))
        
        return Response({
            'total': {'count': total},
            'open': {'count': open_count},
            'resolved': {'count': resolved_count},
            'byCategory': by_category
        })
