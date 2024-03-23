from django.shortcuts import render

from .models import Card

def easy_random_card(request):
    card = Card.objects.filter(level='easy').order_by('?').first()
    return render(request, 'card.html', {'card': card})

def intermediate_random_card(request):
    card = Card.objects.filter(level='intermediate').order_by('?').first()
    return render(request, 'card.html', {'card': card})

def advanced_random_card(request):
    card = Card.objects.filter(level='advanced').order_by('?').first()
    return render(request, 'card.html', {'card': card})