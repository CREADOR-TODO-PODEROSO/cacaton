import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Accion

def load_actions():
    acciones = [
        {"nombre": "Buscar Leña", "impacto_temperatura": -5, "impacto_energia": -15},
        {"nombre": "Encender Fogata", "impacto_temperatura": 20, "impacto_energia": -5},
        {"nombre": "Construir Refugio", "impacto_temperatura": 10, "impacto_energia": -25},
        {"nombre": "Descansar", "impacto_temperatura": -2, "impacto_energia": 30},
    ]

    for a in acciones:
        Accion.objects.get_or_create(**a)
    print("✅ Acciones de supervivencia creadas con éxito.")

if __name__ == '__main__':
    load_actions()