from flask import Blueprint, render_template, request, jsonify
from .services import get_spotify_token, search_song
import requests
from requests.auth import HTTPBasicAuth

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/search', methods=['POST'])
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

@main.route('/track/<track_id>', methods=['GET'])
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