

#  Frozen Escape API - Hackathon Survival

##  Descripción

[cite_start]**Frozen Escape** es una API REST desarrollada con **Django** y **Django REST Framework** que simula un juego de supervivencia en condiciones extremas de frío [cite: 154-156]. [cite_start]El usuario debe gestionar su temperatura corporal y energía tomando decisiones estratégicas (acciones) para mantenerse con vida el mayor tiempo posible 

##  Tecnologías Utilizadas

  * [cite_start]**Backend:** Django 6.0
  * [cite_start]**API:** Django REST Framework (DRF)
  * **Documentación:** Swagger (drf-yasg).
  * [cite_start]**Base de Datos:** SQLite (Persistencia de datos)

-----

##  Instrucciones de Ejecución

Sigue estos pasos para poner en marcha el simulador en tu entorno local:

### 1\. Clonar y Preparar el Entorno

```bash
# Clonar el repositorio 
git clone https://github.com/CREADOR-TODO-PODEROSO/cacaton.git
cd hackathon_survival

# Crear y activar entorno virtual
python -m venv env
# En Windows:
.\env\Scripts\activate
# En Linux/Mac:
source env/bin/activate

# Instalar dependencias
pip install django djangorestframework drf-yasg django-cors-headers
```

### 2\. Configurar la Base de Datos

Es necesario aplicar las migraciones para crear las tablas de Usuarios, Acciones y Estado del Jugador 

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3\. Cargar Datos Iniciales (Seed)

He incluido un script para cargar automáticamente las acciones de supervivencia necesarias para jugar

```bash
python seed.py
```

### 4\. Iniciar el Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

-----

##  Guía de Pruebas (Endpoints)

Puedes probar la lógica completa desde la documentación interactiva en:
 **[http://127.0.0.1:8000/docs/](https://www.google.com/search?q=http://127.0.0.1:8000/docs/)**

### Flujo de Juego Recomendado:

1.  **Registro de Usuario (`POST /api/usuario/`)**: Crea un usuario con `username` y `password`. [cite_start]Esto genera automáticamente su estado inicial (37°C de temperatura y 100% de energía)
2.  [cite_start]**Ver Acciones (`GET /api/acciones/`)**: Consulta el catálogo de acciones disponibles y anota sus IDs 
3.  **Ejecutar Acción (`POST /api/juego/{id}/ejecutar_accion/`)**: Envía el `accion_id` para afectar el estado de tu sobreviviente.
      * [cite_start]*Nota:* La lógica incluye un **componente aleatorio** que varía el impacto base de cada acción
4.  [cite_start]**Ranking (`GET /api/usuario/`)**: Lista a los sobrevivientes que aún están con vida, ordenados por sus recursos recolectados 
-----

##  Lógica del Sistema

  * [cite_start]**Condición de Derrota:** El jugador pierde automáticamente si su **temperatura** o su **energía** llega a cero o menos
  * [cite_start]**Relaciones entre Tablas:** La actualización del estado se realiza mediante una relación `OneToOne` entre el modelo `User` y `EstadoJugador`
  * [cite_start]**Validación:** No se permite ejecutar acciones si el jugador ya ha fallecido



**Desarrollado por:** Jorge Crucerira - ADSO SENA (Ficha 3064975)
                      Melva Ceron
                      Tatiana Ruco


1. Configuración Inicial (Seed Data)
Antes de probar la API, debemos tener "Acciones" en la base de datos.

Acción: Ejecuta en tu terminal python seed.py.


Resultado: Se crearán acciones como "Buscar Leña" (ID: 1) o "Encender Fogata" (ID: 2) .

2. Registro de Usuario (Crear Sobreviviente)
Este endpoint crea el usuario y, mediante la lógica que pusimos en el serializador, genera automáticamente su EstadoJugador inicial .

Método: POST

URL: http://127.0.0.1:8000/api/usuario/

Body (JSON):

JSON
{
    "username": "satan",
    "password": "9090"
}
Qué observar: En la respuesta verás el objeto "estado": {"temperatura": 37, "energia": 100, ...}. Esto confirma que la relación Uno a Uno se creó correctamente .

3. Listar Acciones Disponibles
Antes de jugar, el cliente debe saber qué puede hacer.

Método: GET

URL: http://127.0.0.1:8000/api/acciones/

Body: No requiere.

Qué observar: Una lista de todas las acciones con sus impactos de temperatura y energía. Anota el id de la acción que quieras probar.

4. Ejecutar Acción (Lógica de Supervivencia)
Aquí es donde ocurre la magia del juego y se aplica el componente aleatorio.

Método: POST

URL: http://127.0.0.1:8000/api/juego/{id_del_usuario}/ejecutar_accion/

Body (JSON):

JSON
{
    "accion_id": 2
}
(Nota: Cambia el 2 por el ID de la acción "Encender Fogata" o la que desees).


Qué observar: * La respuesta dirá "Has ejecutado: Encender Fogata" .

Verás que los valores de temperatura y energia cambiaron.


Prueba de Aleatoriedad: Repite el mismo POST varias veces; verás que los números no siempre cambian en la misma cantidad exacta debido al factor de suerte (0.8 a 1.2) que programamos.

5. Ranking de Supervivencia
Muestra quiénes están liderando la supervivencia (ordenados por recursos) .

Método: GET

URL: http://127.0.0.1:8000/api/usuario/

Body: No requiere.

Qué observar: Una lista de usuarios. Solo aparecerán los que tengan esta_vivo: true.

6. Prueba de Muerte (Condición de Derrota)
Obligatorio para demostrar la lógica del sistema.

Usa el endpoint de Ejecutar Acción.

Envía repetidamente una acción que reste mucha energía (como "Buscar Leña", ID: 1).

Resultado esperado: Cuando energia llegue a 0 o menos, la respuesta cambiará a:

JSON
{
    "resultado": "Has muerto por las condiciones extremas.",
    "estado_actual": {
        "temperatura": X,
        "energia": 0,
        "vivo": false
    }
}
Si intentas ejecutar otra acción con ese mismo usuario, la API te devolverá un error: "El jugador ya ha muerto congelado".