from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:group>/', views.get_random_card, name='group'),
]
