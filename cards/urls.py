from django.urls import path
from . import views

urlpatterns = [
    path('easy', views.easy_random_card, name='easy_random_card'),
    path('intermediate', views.intermediate_random_card, name='intermediate_random_card'),
    path('advanced', views.advanced_random_card, name='advanced_random_card'),
]