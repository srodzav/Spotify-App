# Spotify App

Esta es una aplicación web que permite buscar canciones en Spotify y guardar tus canciones favoritas. La aplicación está construida utilizando Flask para el backend y JavaScript para el frontend.

## Características

- Búsqueda de canciones en Spotify por nombre.
- Mostrar resultados de búsqueda con detalles de la canción, como el nombre del artista, nombre de la canción, imagen y un enlace para escuchar la canción en Spotify.
- Agregar canciones a una lista de favoritos almacenada en localStorage.
- Filtrar canciones por artista o nombre.
- Ver y gestionar las canciones favoritas.

## Tecnologías Utilizadas

- Flask
- JavaScript
- HTML
- CSS
- Bootstrap
- Spotify API

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- Python 3.x
- pip (gestor de paquetes de Python)
- Spotify Developer Account para obtener CLIENT_ID y CLIENT_SECRET

## Instalación

1. Clona el repositorio:
```
   git clone https://github.com/tu_usuario/spotify-app.git
   cd spotify-app
```
2. Crea un entorno virtual y actívalo:
```
   python -m venv env
   source env/bin/activate   # En Windows usa `env\Scripts\activate`
```
3. Instala las dependencias:
```
   pip install -r requirements.txt
```

4. Configura las credenciales de Spotify:
   - Crea un archivo `.env` en el directorio raíz del proyecto y añade tus credenciales de Spotify:
     CLIENT_ID=tu_client_id
     CLIENT_SECRET=tu_client_secret

5. Inicia la aplicación Flask:
```
   flask run
```

6. Abre tu navegador y ve a ```http://127.0.0.1:5000``` para ver la aplicación en funcionamiento. 

## Estructura del Proyecto

- static/css/styles.css: Archivos CSS personalizados.
- static/js/scripts.js: Archivos JavaScript personalizados.
- templates/index.html: Archivo HTML principal de la aplicación.
- app.py: Archivo principal de la aplicación Flask.
- .env: Archivo de configuración de entorno (no incluido en el repositorio).
- .gitignore: Archivo para ignorar archivos y carpetas específicos en el control de versiones.
- requirements.txt: Archivo de dependencias de Python.
- README.md: Documentación del proyecto.

# Uso

## Búsqueda de Canciones

1. Ingresa el nombre de la canción en el campo de búsqueda y presiona el botón "Buscar".
2. La aplicación mostrará los resultados de la búsqueda en una tabla.

## Favoritos

1. Para agregar una canción a tus favoritos, presiona el botón "Favorito" junto a la canción en los resultados de búsqueda.
2. Para ver tus canciones favoritas, desplázate hacia abajo hasta la sección "Canciones Favoritas".
3. Para eliminar una canción de tus favoritos, presiona el botón "Quitar" junto a la canción en la lista de favoritos.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.
