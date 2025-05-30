from rest_framework import serializers
from .models import Card, CardGroup


class CardGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardGroup
        fields = ['id', 'name', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CardSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Card
        fields = [
            'uuid', 'name', 'group', 'group_name', 'description', 
            'image', 'created_at', 'updated_at', 'user', 'user_username', 'status'
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']


class CardCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for card creation with minimal required fields"""
    
    class Meta:
        model = Card
        fields = ['name', 'group', 'description', 'image', 'status']