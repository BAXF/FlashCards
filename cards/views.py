from django.shortcuts import render, get_object_or_404

from .models import Card, CardGroup

def get_random_card(request, group):
    # Get the CardGroup object by name
    card_group = get_object_or_404(CardGroup, name=group)
    # Get a random card from the group
    card = Card.objects.filter(group=card_group).order_by('?').first()
    return render(request, 'card.html', {'card': card})

def home(request):
    card_groups = CardGroup.objects.all()
    return render(request, 'home.html', {'card_groups': card_groups})
