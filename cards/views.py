from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Card, CardGroup
from .serializers import CardSerializer, CardGroupSerializer, CardCreateSerializer


def get_random_card(request, group):
    # Get the CardGroup object by name (case-insensitive)
    card_group = get_object_or_404(CardGroup, name__iexact=group)
    # Get a random card from the group
    card = Card.objects.filter(group=card_group).order_by('?').first()
    return render(request, 'card.html', {'card': card})

def home(request):
    card_groups = CardGroup.objects.all()
    return render(request, 'home.html', {'card_groups': card_groups})


# API Views
class CardGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing card groups.
    Provides CRUD operations for card groups.
    """
    queryset = CardGroup.objects.all()
    serializer_class = CardGroupSerializer

    @action(detail=True, methods=['get'])
    def cards(self, request, pk=None):
        """Get all cards in a specific group"""
        group = self.get_object()
        cards = Card.objects.filter(group=group)
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing cards.
    Provides CRUD operations for cards.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_serializer_class(self):
        """Use different serializers for create vs other actions"""
        if self.action == 'create':
            return CardCreateSerializer
        return CardSerializer

    def perform_create(self, serializer):
        """Automatically assign a user when creating a card via API"""
        # Try to use the authenticated user, or get/create a default user for API access
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            # For unauthenticated API access, try to get or create a default user
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username='api_user',
                defaults={
                    'email': 'api@flashcards.local',
                    'first_name': 'API',
                    'last_name': 'User'
                }
            )
        
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def by_group(self, request):
        """Get cards filtered by group"""
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response(
                {'error': 'group_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cards = Card.objects.filter(group_id=group_id)
        serializer = self.get_serializer(cards, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def random(self, request):
        """Get a random card, optionally from a specific group"""
        queryset = Card.objects.all()
        group_id = request.query_params.get('group_id')
        
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        
        card = queryset.order_by('?').first()
        if not card:
            return Response(
                {'message': 'No cards found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(card)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search cards by name or description"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'q parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cards = Card.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        serializer = self.get_serializer(cards, many=True)
        return Response(serializer.data)
