from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Accion, EstadoJugador

class AccionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Accion.
    Convierte las instancias del modelo Accion a formato JSON y viceversa.
    """
    class Meta:
        model = Accion
        fields = '__all__' # Incluye todos los campos del modelo original

class EstadoJugadorSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo EstadoJugador.
    Define qué campos del estado del jugador serán expuestos a través de la API al cliente.
    """
    class Meta:
        model = EstadoJugador
        # Solo exponemos los atributos relevantes para la supervivencia del jugador
        fields = ['temperatura', 'energia', 'recursos', 'esta_vivo']

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de usuario estándar (User) de Django.
    Permite registrar nuevos usuarios y mostrar la información básica junto con su estado en el juego.
    """
    # Incluimos el estado del jugador usando la relación OneToOne (uno a uno) definida en el modelo.
    # Es de solo lectura (read_only=True) para que no se pueda modificar el estado del usuario directamente al registrarse.
    estado = EstadoJugadorSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'estado']
        # La contraseña solo se usa para escribir (crear cuenta o cambiar clave) y nunca se devuelve en respuestas de lectura HTTP
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Sobrescribe el método de creación por defecto para añadir lógica adicional de inicialización.
        Asegura que la contraseña se encripta de forma segura a través del ORM de Django (en lugar de texto plano)
        y que se genera el estado inicial del jugador para empezar la partida.
        """
        # Creamos el usuario encapsulando el hasheo/encriptado de la contraseña
        user = User.objects.create_user(**validated_data)
        
        # Requisito: Crear automáticamente el estado inicial al crear el usuario
        # Inicializamos y asociamos el usuario creado con una nueva instancia de 'EstadoJugador' en BD
        EstadoJugador.objects.create(usuario=user)
        
        return user