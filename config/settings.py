"""
Django settings for config project.
Generadas a través de 'django-admin startproject'.

Contiene cada una de las configuraciones y variables de entorno que dictan el comportamiento a lo ancho y largo de la aplicación principal y las sub-aplicaciones.
"""

from pathlib import Path

# BASE_DIR: Ruta de nivel superior o raíz estática. Todas las referencias a bases de datos en archivo
# o carpetas locales subyacentes se anexan basándose en la resolución de esta variable en el SO actual.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: Combinación encriptada, de carácter ultra-secreto (por favor ignórela fuera de dev).
# Se utiliza para salar información, validar hashes para contraseñas de las cuentas de usuario y salvaguardar las cookies de sesión del juego frente a alteraciones perversas online.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d1mx-_dlw&_uh5ckyzp0xsv!0=sdf8s3_x3%+*o7+ph3vv0v@^'

# DEBUG: Estatus global del modo local. Si está inicializado en True se dispararán pantallas de rastreo/stack-traces con métricas al haber colapsos. 
# Si se pone en un servidor productivo se deben sustituir a False de manera innegociable.
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS: Arreglo limitante de strings que define un factor "whitelist" con aquellos Dominios u Orígenes desde
# los que este proyecto puede transaccionar un requerimiento GET/POST de manera confiable. Si está vacío, por omisión soporta los locales para desarrollo y nada de internet externo.
ALLOWED_HOSTS = []


# Application definition

# INSTALLED_APPS: Bloque fundamental para la escalabilidad.
# Cada vez que creamos un ecosistema nuevo de código (como la carpeta /core con la app respectiva), o si se instalan librerías para la API mediante pip install (como rest_framework para APIs o drf_yasg para mapear el Swagger), necesitamos declarar el título de las mismas en el pool virtual para que se registren a nivel persistente con el ORM del framework.
INSTALLED_APPS = [
    # Paquetes originales de la suite nativa de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Paquetes Third-party externos para extender la matriz de funcionalidades en REST
    'rest_framework',
    'drf_yasg',

    # Bloque de Aplicaciones Custom elaboradas de cero (donde se sitúa el corazón o el núcleo de nuestra lógica Hackathon)
    'core',
]

# MIDDLEWARE: Capa de clases interpretativas que se paran de forma omnipresente interceptando la llamada u obispo entre el cliente externo y la llegada a nuestra view.py.
# Son escudos y procesadores en serie, de seguridad básica al lidiar con cross origin logic, validadores de sesiones, o prevención tipo CSRF para las vulneraciones a inyecciones.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Constante en la forma de String con notación de punto para apuntar a la variable (URLconf) encargada del mapeo direccional y del enrutamiento de nuestro servicio entero.
ROOT_URLCONF = 'config.urls'

# TEMPLATES: Motor de plantillas o renderizador. 
# No se utilizará con mucho peso dado a la naturaleza separada (backend que devuelve objetos JSON como Rest API).
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Objeto global base invocado subyacentemente al instanciar Gunicorn (para deployments a prod via Python Server Gateway Interfaces).
WSGI_APPLICATION = 'config.wsgi.application'


# Database
# DATABASES: Entorno definitorio de bases de datos, contraseñas de las mismas o IP's de sockets.
# Como pauta genérica transigente inicial se deja a la "SQLite3" la cual trabaja al compilar en vivo escribiendo un registro de archivo simple denominado 'db.sqlite3' dentro del proyecto. De requerirse Postgresql acá se altera el ENGINE a base y el string de conexion con las credentials.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# AUTH_PASSWORD_VALIDATORS: Capa intrínseca que somete bajo escrutinio al conjunto y orden de letras de un Password para ver si acatan el criterio mínimo que dicta la ley contra amenazas comunes del día a día (Bruteforce y Dictionary attacks en logins).
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# Reguladores de dialecto, idioma, región y zonas estandarizadas para trabajar conversiones de fechas.
LANGUAGE_CODE = 'es' # Lo editamos a sistema del Español predeterminado

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# STATIC_URL: Variable de terminación virtual (donde va a vivir la imagen/CSS montada o expuesta en browser para la API)
STATIC_URL = 'static/'
