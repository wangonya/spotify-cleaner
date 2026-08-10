import os
from pathlib import Path

_ENV_PATH = Path(__file__).with_name(".env")
if _ENV_PATH.exists():
    for line in _ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise SystemExit(
        "Error: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables must be set."
    )

SCOPE = "user-library-read user-library-modify playlist-read-private playlist-modify-private playlist-modify-public user-read-playback-position"
REDIRECT_URI = "http://127.0.0.1:8080/callback"  # Spotify rejects "localhost"
BASE_URL = "https://api.spotify.com/v1"

RESPONSE_ITEMS_LIMIT = 50  # Number of items to fetch per request. MIN: 0, MAX: 50
LIBRARY_ITEMS_LIMIT = 40  # Max URIs per DELETE /me/library request

URI_TYPE = {
    "tracks": "track",
    "albums": "album",
    "shows": "show",
    "episodes": "episode",
    "playlists": "playlist",
}

TEMPLATE_AUTH_KWARGS = {
    "CLIENT_ID": CLIENT_ID,
    "REDIRECT_URI": REDIRECT_URI,
    "SCOPE": SCOPE,
}
