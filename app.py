from flask import Flask, request, render_template, jsonify
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Credenciales para utilizar API de Spotify
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Funcion para obtener el token de acceso
def get_spotify_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET) # Usuario sin necesidad de login
    response = requests.post(url, headers=headers, data=data, auth=auth)
    return response.json()['access_token']

# Funcion para buscar canciones en Spotify
def search_song(query, token):
    url = f'https://api.spotify.com/v1/search?q={query}&type=track' # Podemos definir limite añadiendo: '&limit=10'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Ruta INDEX
@app.route('/')
def index():
    return render_template('index.html')

# Ruta BUSQUEDA
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    token = get_spotify_token()
    results = search_song(query, token)
    tracks = []
    for item in results['tracks']['items']:
        tracks.append({
            'artist': item['artists'][0]['name'],
            'name': item['name'],
            'image': item['album']['images'][0]['url'],
            'url': item['external_urls']['spotify']
        })
    return jsonify(tracks)

# Ruta obtener TRACK mediante TRACK_ID
@app.route('/track/<track_id>', methods=['GET'])
def get_track(track_id):
    token = get_spotify_token()
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        track_data = response.json()
        track_info = {
            'artist': track_data['artists'][0]['name'],
            'name': track_data['name'],
            'image': track_data['album']['images'][0]['url'],
            'url': track_data['external_urls']['spotify']
        }
        return jsonify(track_info)
    else:
        return jsonify({'error': 'Track not found'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
