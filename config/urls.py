"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configuración de la vista de esquema (Schema View) para la documentación de la API externa a través de Swagger.
# Sirve como hub de lectura para cualquier persona que consuma la API, construyendo reportes en tiempo real según los serializadores y endpoints que existan.
schema_view = get_schema_view(
    openapi.Info(
        title="Frozen Escape API",
        default_version='v1',
        description="API de supervivencia en condiciones extremas y gestión de recursos.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), # Configura que cualquier persona (inclusive anónimos) pueda consultar la documentación
)

# Raíz principal de la aplicación.
# En lugar de registrar vistas aisladas de manera rígida acá, Django recomienda el "include()"
urlpatterns = [
    # Ruta clásica hacia el panel administrativo privado provisto nativo en Django
    path('admin/', admin.site.urls),
    
    # Endpoints del ecosistema del juego.
    # Cualquier comunicación al backend que arranque con la estructura URI "/api/..."
    # será transferida jerárquicamente a evaluarse en las URLs del archivo local de la app core.
    path('api/', include('core.urls')),
    
    # Páginas automáticas que corren la UI visual de la librería drf_yasg para lectura del esquema (Swagger UI).
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # Interfaz equivalente del API pero rendida en el formato rediseñado de "Redoc".
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
