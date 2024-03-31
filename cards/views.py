from django.shortcuts import render

from .models import Card, CardGroup

def get_random_card(request, group):
    # this will get a random card from the group
    card = Card.objects.filter(group=group).order_by('?').first()
    return render(request, 'card.html', {'card': card})

def home(request):
    card_groups = CardGroup.objects.all()
    return render(request, 'home.html', {'card_groups': card_groups})
