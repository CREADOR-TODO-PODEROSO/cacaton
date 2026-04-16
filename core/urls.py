from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JuegoViewSet, UsuarioViewSet, AccionViewSet 

# Se utiliza un DefaultRouter de Django Rest Framework para automatizar 
# la generación de URLs estándar para los ViewSets de la aplicación (GET, POST, PUT, DELETE, etc.)
router = DefaultRouter()

# Endpoints requeridos por la Hackathon 
# Registramos las vistas principales (ViewSets) dentro del router.
# La función de 'ejecutar_accion' estará disponible dentro de /juego/{id_usuario}/ejecutar_accion
router.register(r'juego', JuegoViewSet, basename='juego')

# La ruta /usuario/ habilitará el registro de usuarios y el listado para el mecanismo de "ranking"
router.register(r'usuario', UsuarioViewSet, basename='usuario') 

# La ruta /acciones/ ofrecerá un listado solo lectura de los movimientos viables para el jugador
router.register(r'acciones', AccionViewSet, basename='acciones')

urlpatterns = [
    # Se incluyen todas las URLs autogeneradas en el nivel raíz de esta aplicación.
    # Así, si esta app se monta bajo /api/ en el archivo principal de configuración,
    # tendremos /api/juego/, /api/usuario/ y /api/acciones/ inmediatamente disponibles.
    path('', include(router.urls)),
]