// Arreglos de canciones
let tracks = [];
let originalTracks = [];

async function buscarCancion() {
    const query = document.getElementById('query').value;
    const response = await fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `query=${query}`
    });
    const data = await response.json();
    tracks = data;
    originalTracks = [...data];
    mostrarCanciones(tracks);
    cargarArtistasUnicos(tracks);
    cargarFavoritos();
    document.getElementById('query').value = '';
}

function mostrarCanciones(tracks) {
    const table = document.getElementById('results');
    table.innerHTML = '';
    tracks.forEach(track => {
        const row = document.createElement('tr');
        // Desglosamos track.url para poder insertarlo como widget.
        const trackId = track.url.split('/').pop();
        const iframeSrc = `https://open.spotify.com/embed/track/${trackId}`;
        // Cargamos datos
        row.innerHTML = `
            <td class="irrelevance"> ${track.artist} </td>
            <td class="irrelevance" style="max-width: 150px;"> ${track.name} </td>
            <td class="irrelevance"> <img src="${track.image}" width="50"> </td>
            <td class="priority">
                <iframe style="border-radius:12px" src="${iframeSrc}" width="100%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            </td>
            <td class="priority">
                <button type="button" class="btn btn-success mr-1" onclick="addToFavorites('${trackId}')" title="Bookmark">
                    <i class="bi bi-bookmark-star-fill"></i>
                </button>
                <button type="button" class="btn btn-danger mr-1" onclick="ocultar(this)" title="Hide">
                    <i class="bi bi-slash-circle"></i>
                </button>
            </td>

        `;
        table.appendChild(row);
    });
}

function cargarArtistasUnicos(tracks) {
    const artistSelect = document.getElementById('artistFilter');
    artistSelect.innerHTML = '<option value="">All Artists</option>'; // Opción por defecto
    const artistasUnicos = [...new Set(tracks.map(track => track.artist))]; // no se repiten artistas
    artistasUnicos.forEach(artist => {
        const option = document.createElement('option');
        option.value = artist;
        option.textContent = artist;
        artistSelect.appendChild(option);
    });
}

function filtrarCanciones() {
    const artistFilter = document.getElementById('artistFilter').value.toLowerCase();
    const songFilter = document.getElementById('songFilter').value.toLowerCase();
    const filteredTracks = tracks.filter(track => 
        track.artist.toLowerCase().includes(artistFilter) &&
        track.name.toLowerCase().includes(songFilter)
    );
    mostrarCanciones(filteredTracks);
}

function ocultar(button) {
    button.closest('tr').style.display = 'none';
}

function reiniciarTabla() {
    tracks = [...originalTracks];
    mostrarCanciones(tracks);
    document.getElementById('artistFilter').value = '';
    document.getElementById('songFilter').value = '';
}

function mostrarJSON() {
    const jsonContent = document.getElementById('jsonContent');
    jsonContent.textContent = JSON.stringify(tracks, null, 2); // Rellena el contenido del modal

    // Mostrar el modal usando la API de Bootstrap 5
    const modal = new bootstrap.Modal(document.getElementById('jsonModal'));
    modal.show();
}

function addToFavorites(trackId) {
    let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    console.log(favorites, trackId);
    if (!favorites.includes(trackId)) { // Se guarda solamente track_id
        favorites.push(trackId);
        localStorage.setItem('favorites', JSON.stringify(favorites));
        showAlert('Added to favorites!', 'success');
        cargarFavoritos(); // Recargar la lista de favoritos
    } else {
        showAlert('Already in favorites!', 'warning');
    }
}

async function cargarFavoritos() {
    const favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    const container = document.getElementById('favorites');
    container.innerHTML = ''; // Limpia los favoritos antes de recargar

    for (const trackId of favorites) {
        const track = await obtenerTrack(trackId);

        if (trackId) {
            const iframeSrc = `https://open.spotify.com/embed/track/${trackId}`;
            // Crear la tarjeta con Bootstrap
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="irrelevance">${track.artist}</td>
                <td class="irrelevance" style="max-width: 150px;">${track.name}</td>
                <td class="irrelevance"><img src="${track.image}" width="50"></td>
                <td class="priority">
                    <iframe style="border-radius:12px" src="${iframeSrc}" width="100%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                </td>
                <td class="priority">
                    <button onclick="removeFromFavorites('${trackId}')" class="btn btn-danger" title="Unmark"><i class="bi bi-trash3-fill"></i></button>
                </td>
            `;
            container.appendChild(row);
        }
    }
}

async function obtenerTrack(trackId) {
    // Primero buscamos en tracks cargados
    let track = tracks.find(t => t.url.split('/').pop() === trackId);
    // Si no encontramos, buscamos mediante la API
    if (!track) {
        const response = await fetch(`/track/${trackId}`);
        track = await response.json();
    }
    return track;
}

function removeFromFavorites(trackId) {
    let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    favorites = favorites.filter(fav => fav !== trackId);
    localStorage.setItem('favorites', JSON.stringify(favorites));
    cargarFavoritos();
    showAlert('Removed from favorites!', 'success');
}

function showAlert(message, type = 'success') {
    const icons = {
        success: '#check-circle-fill',
        info: '#info-fill',
        warning: '#exclamation-triangle-fill',
        danger: '#exclamation-triangle-fill',
    };

    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show d-flex align-items-center`;
    alert.role = 'alert';

    alert.innerHTML = `
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="${type}:">
            <use xlink:href="${icons[type]}"></use>
        </svg>
        <div>${message}</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const container = document.getElementById('alert-container');
    container.appendChild(alert);

    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 150);
    }, 3000);
}

function toggleResults() {
    const resultsCollapse = document.getElementById('resultsCollapse');
    const collapseInstance = new bootstrap.Collapse(resultsCollapse);
    collapseInstance.toggle();
}

document.getElementById('resultsCollapse').addEventListener('hidden.bs.collapse', function () {
    const btn = document.getElementById('toggleResultsBtn');
    btn.innerHTML = '<i class="bi bi-chevron-down"></i> Show Results';
});

document.getElementById('resultsCollapse').addEventListener('shown.bs.collapse', function () {
    const btn = document.getElementById('toggleResultsBtn');
    btn.innerHTML = '<i class="bi bi-chevron-up"></i> Hide Results';
});


document.addEventListener('DOMContentLoaded', function() {
    cargarFavoritos();
});

document.getElementById('query').value = '';

document.getElementById('year').textContent = new Date().getFullYear();