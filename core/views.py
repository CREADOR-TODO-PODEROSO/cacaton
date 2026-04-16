import random
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Accion, EstadoJugador
from .serializers import UsuarioSerializer, AccionSerializer
from django.contrib.auth.models import User
from rest_framework import permissions

class AccionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar las acciones disponibles (GET /api/acciones/).
    Al extender de ReadOnlyModelViewSet, garantiza que a través de este endpoint 
    únicamente se puedan consultar elementos mediante GET list/retrieve, pero NO 
    crear, alterar ni borrar. Como son fijas y se cargan mediante un semillero (seed), es idóneo.
    """
    queryset = Accion.objects.all()
    serializer_class = AccionSerializer

class JuegoViewSet(viewsets.GenericViewSet):
    """
    ViewSet que agrupa la lógica en tiempo real para las peticiones del juego.
    No sigue el formato CRUD usual, sino que utiliza funciones englobadoras
    gracias a la herencia de GenericViewSet y decoradores @action.
    """
    
    # Detalla un endpoint adicional, que responderá sólo a peticiones POST 
    # de tipo /api/juego/<pk>/ejecutar_accion/, donde <pk> indica el ID del jugador
    @action(detail=True, methods=['post'])
    def ejecutar_accion(self, request, pk=None):
        """
        Recibe e interpreta qué acción decidió llevar cabo el jugador, calcula
        el impacto sobre su temperatura y energía, y juzga si el personaje fallece.
        """
        # Se obtiene el estatus general vinculante al ID que viajó a través de la URL.
        estado = EstadoJugador.objects.get(usuario_id=pk)
        
        # Como primera regla de negocio, verificamos si el jugador aún tiene el flag de 'vivo'.
        if not estado.esta_vivo:
            return Response({"error": "El jugador ya ha muerto congelado."}, status=status.HTTP_400_BAD_REQUEST)

        # De los datos JSON en el cuerpo del POST, buscamos qué identificador de Acción solicitan aplicar.
        accion_id = request.data.get('accion_id')
        try:
            accion = Accion.objects.get(id=accion_id)
        except Accion.DoesNotExist:
            return Response({"error": "Acción no válida"}, status=status.HTTP_400_BAD_REQUEST)

        # Lógica con componente aleatorio que simula la fortuna en un momento de presión,
        # arrojando un multiplicador volátil entre el 80% y 120%.
        suerte = random.uniform(0.8, 1.2)
        
        # Se aplican los cambios a la temperatura o a la energía, multiplicados por el RNG.
        estado.temperatura += int(accion.impacto_temperatura * suerte)
        estado.energia += int(accion.impacto_energia * suerte)

        # Regla de derrota de la hackathon: 
        # Si las métricas de supervivencia bajan peligrosamente hasta el 0 o los negativos, el estado falla permanentemente.
        if estado.temperatura <= 0 or estado.energia <= 0:
            estado.esta_vivo = False
            mensaje = "Has muerto por las condiciones extremas."
        else:
            mensaje = f"Has ejecutado: {accion.nombre}"

        # Consignamos explícitamente en BD el nuevo estado con sus recálculos estadísticos.
        estado.save() 
        
        # Envoltorio en formato JSON respondiendo siempre con qué pasó en la fase ("mensaje")
        # y cómo quedó el saldo final de stats para visualizarlos de modo inmediato en el Front-End.
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
    ViewSet que centraliza el modelo de usuarios del juego (Frozen Escape).
    Permitiendo la vista al catálogo, el acceso general al ranking, y que nuevos jugadores 
    manden un registro POST a la dirección /api/usuario/.
    """
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    # Permite acceso incondicionalmente a todos (Auth no requerido), para el flujo del juego
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Anula/Redefine el set de datos que entrega un GET global (listado).
        En nuestro requerimiento esto se usa como Ranking: 
        Se filtra con doble guion bajo ('estado__esta_vivo') para entrar en la foreing-key de la 
        tabla relacionada EstadoJugador y confirmar que solo se muestre en pantalla los supervivientes, 
        y se decreta un ORDER BY DESC por la variable de recursos para que el de mayor recurso encabece la lista.
        """
        return User.objects.filter(estado__esta_vivo=True).order_by('-estado__recursos')