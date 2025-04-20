
# Spotify Music Snapshot

Generate a private Spotify playlist of your top 50 tracks (titled with today’s date and described by your top 5 artists) via a simple web app.

---

## Architecture

```
repo-root/
├── backend/   # Flask API (OAuth, playlist logic)
└── frontend/  # React UI (button, status, styling)
```

---

## Prerequisites

- **Node.js** (with npm)  
- **Python 3.8+** (with pip)  
- A **Spotify Developer** app (Client ID & Secret)

---

## Quick Start

1. **Clone & configure**  
   ```bash
   git clone https://github.com/<YOU>/spotifyMusicSnapshot.git
   cd spotifyMusicSnapshot
   ```
2. **Backend**  
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env        # fill in your Spotify credentials + URIs
   python app.py               # starts API on http://localhost:5000
   ```
3. **Frontend**  
   ```bash
   cd ../frontend
   npm install
   npm start                   # opens UI on http://localhost:3000
   ```
4. **Use it!**  
   - Visit the UI, click **Create playlist**,  
   - Authorize in Spotify if prompted,  
   - See a success message with an **Open new playlist** button.

---

## Deployment (Render.com)

1. Push this repo to GitHub.  
2. On Render:
   - **Web Service** → point at `backend/`, build with `pip install…`, start with `gunicorn app:app`, add your env vars.  
   - **Static Site** → point at `frontend/`, build with `npm run build`, publish the `build/` folder.  
3. Update your Spotify app’s Redirect URI to your Render API URL (`…/callback`).  

Your live site will then let anyone generate their own Spotify snapshot in just two clicks.

---

## Env Vars

Set these (locally in `.env` or on your host):

```
FLASK_SECRET_KEY
SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET
SPOTIFY_REDIRECT_URI     # e.g. https://<api>.onrender.com/callback
FRONTEND_URI             # e.g. https://<ui>.onrender.com
```
