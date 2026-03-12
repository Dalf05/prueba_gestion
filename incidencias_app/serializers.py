from rest_framework import serializers
from .models import Incident, Comment

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'user_name']

    def get_user_name(self, obj):
        return obj.user.username if obj.user else "Usuario"

class IncidentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Incident
        fields = '__all__'
