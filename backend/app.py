import os
import base64
import requests
from urllib.parse import urlencode
from flask import Flask, request, redirect, session
from dotenv import load_dotenv

load_dotenv()  # make sure .env is loaded

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

SPOTIFY_CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI          = os.getenv("SPOTIFY_REDIRECT_URI")
FRONTEND_URI          = os.getenv("FRONTEND_URI", "http://localhost:3000")
SCOPE                = "playlist-modify-private user-top-read"

@app.route("/login")
def login():
    # generate a state token to protect against CSRF
    state = os.urandom(16).hex()
    session["state"] = state

    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state,
        "show_dialog": "true"
    }
    auth_url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # 1. Verify state
    if request.args.get("state") != session.get("state"):
        return redirect(f"{FRONTEND_URI}/?error=state_mismatch")

    code = request.args.get("code")

    # 2. Exchange code for tokens
    token_resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        },
        headers={
            "Authorization": "Basic " + base64.b64encode(
                f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()
            ).decode(),
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    if token_resp.status_code != 200:
        return redirect(f"{FRONTEND_URI}/?error=token_exchange_failed")

    tokens = token_resp.json()
    access_token  = tokens["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    # 3. Fetch top tracks + artists, create playlist, add tracks
    me = requests.get("https://api.spotify.com/v1/me", headers=headers).json()
    user_id = me["id"]

    top_tracks = requests.get(
        "https://api.spotify.com/v1/me/top/tracks",
        headers=headers,
        params={"limit": 50, "time_range": "short_term"}
    ).json()
    uris = [t["uri"] for t in top_tracks["items"]]

    top_artists = requests.get(
        "https://api.spotify.com/v1/me/top/artists",
        headers=headers,
        params={"limit": 5, "time_range": "short_term"}
    ).json()
    desc = ", ".join([a["name"] for a in top_artists["items"]])

    # create the playlist
    from datetime import datetime
    today = datetime.now().strftime("%B %d, %Y")
    payload = {"name": today, "description": desc, "public": False}
    print("▶️ Creating playlist with payload:", payload)
    playlist_resp = requests.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        headers=headers,
        json=payload
    )
    print("▶️ Spotify replied:", playlist_resp.status_code, playlist_resp.json())
    if playlist_resp.status_code != 201:
        return redirect(f"{FRONTEND_URI}/?error=playlist_creation_failed")

    playlist_id  = playlist_resp.json()["id"]
    add_resp = requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json={"uris": uris}
    )
    if add_resp.status_code != 201:
        return redirect(f"{FRONTEND_URI}/?error=track_add_failed")

    # 4. Everything succeeded—redirect to React with the new playlist URL
    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
    return redirect(f"{FRONTEND_URI}/?playlist_url={playlist_url}")

if __name__ == "__main__":
    app.run(port=5000)
