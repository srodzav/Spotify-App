# Spotify Demo

This is a web application that integrates with the Spotify API, allowing users to search for songs, manage favorites, and view their Spotify profile.

## Features

- **Spotify OAuth Login**: Secure login using Spotify's API.
- **Song Search**: Search for songs and view details such as album covers and previews.
- **Favorites Management**: Add or remove songs from favorites (stored locally in the browser).
- **Profile Modal**: Displays user profile information (name, email, country, and profile picture) after login.

---

## Technologies Used

**Frontend**

   Hosted at: **spotifydemo.sebastianrdz.com**

   Built with:

   - HTML/CSS/JS: Bootstrap for styling.
   - Local storage for managing favorites.
   - Fetch API for backend communication.

**Backend**

   Hosted at: **PythonAnywhere**

   Built with:
   - Flask: Lightweight Python framework.
   - Spotify API: For song data and authentication.
   - Flask-CORS: To handle cross-origin requests from the frontend.

**Tech Stack**

   **Frontend**: HTML, CSS, JavaScript (Bootstrap)

   **Backend**: Python, Flask.

   **Hosting**:
   - Frontend: DirectAdmin.
   - Backend: PythonAnywhere.

---

# Deployment Instructions

**Backend**

   Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Configure environment variables:
   ```
      CLIENT_ID, CLIENT_SECRET, SECRET_KEY in a .env file.
   ```

   Ensure **wsgi.py** points to the correct app factory.

   Deploy the backend on PythonAnywhere.

**Frontend**

   Place frontend files (HTML, CSS, JS) in the public_html folder of DirectAdmin.

   Update the fetch URLs in main.js to point to the backend's live URL.

## Usage

   Visit spotifydemo.sebastianrdz.com.\
   Log in using your Spotify account.\
   Search for songs or manage your favorites.\
   View your profile in the modal after logging in.

## Notes

   The app requires a Spotify Developer account to configure the CLIENT_ID and CLIENT_SECRET.
   The frontend and backend are hosted on separate domains, so CORS headers are set on the backend.

## Author

**Sebastián Rodríguez**
- [LinkedIn](https://www.linkedin.com/in/sebastian-rodriguez-zavala/)
- [GitHub](https://github.com/srodzav)
- [Email](mailto:contact@sebastianrdz.com)

---

## License

This project is for personal use and is not licensed for commercial distribution.
