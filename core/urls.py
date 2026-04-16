from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JuegoViewSet, UsuarioViewSet, AccionViewSet # Asegúrate de crear UsuarioViewSet en views.py

router = DefaultRouter()
# Endpoints requeridos por la Hackathon 
router.register(r'juego', JuegoViewSet, basename='juego')
router.register(r'usuario', UsuarioViewSet, basename='usuario') # Registro de usuarios y ranking
router.register(r'acciones', AccionViewSet, basename='acciones') # Listado de acciones para el jugador

urlpatterns = [
    path('', include(router.urls)),
]