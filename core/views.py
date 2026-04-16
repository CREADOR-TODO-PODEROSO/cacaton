from django.shortcuts import render

import random
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Accion, EstadoJugador
from .serializers import UsuarioSerializer, AccionSerializer
from django.contrib.auth.models import User
from rest_framework import permissions

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # El ranking debe devolver solo usuarios vivos
        return User.objects.filter(estado__esta_vivo=True).order_by('-estado__recursos')

class AccionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar las acciones disponibles (GET /api/acciones/)
    """
    queryset = Accion.objects.all()
    serializer_class = AccionSerializer

class JuegoViewSet(viewsets.GenericViewSet):
    
    @action(detail=True, methods=['post'])
    def ejecutar_accion(self, request, pk=None):
        estado = EstadoJugador.objects.get(usuario_id=pk)
        
        if not estado.esta_vivo:
            return Response({"error": "El jugador ya ha muerto congelado."}, status=status.HTTP_400_BAD_REQUEST)

        accion_id = request.data.get('accion_id')
        try:
            accion = Accion.objects.get(id=accion_id)
        except Accion.DoesNotExist:
            return Response({"error": "Acción no válida"}, status=status.HTTP_400_BAD_REQUEST)

        # Lógica con componente aleatorio
        suerte = random.uniform(0.8, 1.2)
        estado.temperatura += int(accion.impacto_temperatura * suerte)
        estado.energia += int(accion.impacto_energia * suerte)

        # Regla de derrota 
        if estado.temperatura <= 0 or estado.energia <= 0:
            estado.esta_vivo = False
            mensaje = "Has muerto por las condiciones extremas."
        else:
            mensaje = f"Has ejecutado: {accion.nombre}"

        estado.save() 
        
        return Response({
            "resultado": mensaje,
            "estado_actual": {
                "temperatura": estado.temperatura,
                "energia": estado.energia,
                "vivo": estado.esta_vivo
            }
        })

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar las acciones disponibles en Frozen Escape.
    Usamos ReadOnly porque las acciones se crean por el admin o seed.py.
    """
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Ahora sí, el ranking filtrado por sobrevivientes 
        return User.objects.filter(estado__esta_vivo=True).order_by('-estado__recursos')