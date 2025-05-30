from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for API endpoints
router = DefaultRouter()
router.register(r'cards', views.CardViewSet, basename='card')
router.register(r'groups', views.CardGroupViewSet, basename='cardgroup')

urlpatterns = [
    # Web views
    path('', views.home, name='home'),
    path('<str:group>/', views.get_random_card, name='group'),
    
    # API endpoints
    path('api/', include(router.urls)),
]
