from django.db import models
from django.contrib.auth.models import User

class Accion(models.Model):
    # Definimos los tipos de acciones posibles
    nombre = models.CharField(max_length=100) # Ej: "Encender fogata" [cite: 169]
    impacto_temperatura = models.IntegerField() # Cuánto sube o baja la temperatura [cite: 170]
    impacto_energia = models.IntegerField() # Cuánta energía consume o recupera [cite: 171]

    def __str__(self):
        return self.nombre

class EstadoJugador(models.Model):
    # Relación Uno a Uno: Cada usuario tiene un único estado de juego [cite: 173]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estado')
    
    # Atributos de supervivencia [cite: 174-176]
    temperatura = models.IntegerField(default=37) # Valor inicial normal
    energia = models.IntegerField(default=100)
    recursos = models.IntegerField(default=0)
    dias_sobrevividos = models.IntegerField(default=0) # Para el Ranking [cite: 188]
    esta_vivo = models.BooleanField(default=True)

    def __str__(self):
        return f"Estado de {self.usuario.username}"