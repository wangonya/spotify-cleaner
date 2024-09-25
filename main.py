import requests
from bottle import abort, redirect, request, response, route, run, template

CLIENT_ID = ""  # Your Spotify Client ID
CLIENT_SECRET = ""  # Your Spotify Client Secret
SCOPE = "user-library-read user-library-modify playlist-read-private playlist-modify-private playlist-modify-public"
REDIRECT_URI = "http://localhost:8080/callback"
BASE_URL = "https://api.spotify.com/v1"

RESPONSE_ITEMS_LIMIT = 50  # Number of items to fetch per request. MIN: 0, MAX: 50

TEMPLATE_AUTH_KWARGS = {
    "CLIENT_ID": CLIENT_ID,
    "REDIRECT_URI": REDIRECT_URI,
    "SCOPE": SCOPE,
}


def _get_access_token():
    access_token = request.get_cookie("access_token")
    if access_token is None:
        abort(401, "Error: access_token not provided")

    return access_token


@route("/")
def main():
    return template(
        "home",
        **TEMPLATE_AUTH_KWARGS,
    )


@route("/callback")
def callback():
    code = request.query.code
    if code is None:
        abort(401, "Error: code not provided")

    res = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    if res.status_code != 200:
        abort(res.status_code, res.json()["error_description"])

    response.set_cookie(
        "access_token",
        res.json()["access_token"],
    )
    response.set_cookie(
        "refresh_token",
        res.json()["refresh_token"],
    )

    redirect("/")


def get_offset_based_on_total_and_previous_offset(total, previous_offset):
    return (
        previous_offset + RESPONSE_ITEMS_LIMIT
        if total > previous_offset + RESPONSE_ITEMS_LIMIT
        else None
    )


def _get_items(access_token, item_type, offset, items=None):
    res = requests.get(
        f"{BASE_URL}/me/{item_type}?limit={RESPONSE_ITEMS_LIMIT}&offset={offset}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if res.status_code != 200:
        abort(res.status_code, res.json()["error"]["message"])

    if items is None:
        items = res.json()["items"]
    else:
        items += res.json()["items"]

    if res.json()["total"] > offset + RESPONSE_ITEMS_LIMIT:
        next_offset = get_offset_based_on_total_and_previous_offset(
            res.json()["total"], offset
        )
        if next_offset is not None:
            _get_items(access_token, item_type, next_offset, items)

    return items


@route("/get-liked-songs")
def get_liked_songs():
    access_token = _get_access_token()
    tracks = _get_items(
        access_token,
        "tracks",
        0,
    )

    return template(
        "home",
        tracks=tracks,
        **TEMPLATE_AUTH_KWARGS,
    )


@route("/get-saved-albums")
def get_saved_albums():
    access_token = _get_access_token()
    albums = _get_items(
        access_token,
        "albums",
        0,
    )

    return template(
        "home",
        albums=albums,
        **TEMPLATE_AUTH_KWARGS,
    )


@route("/get-playlists")
def get_playlists():
    access_token = _get_access_token()
    playlists = _get_items(
        access_token,
        "playlists",
        0,
    )

    return template(
        "home",
        playlists=playlists,
        **TEMPLATE_AUTH_KWARGS,
    )


@route("/get-podcasts")
def get_podcasts():
    access_token = _get_access_token()
    shows = _get_items(
        access_token,
        "shows",
        0,
    )

    return template(
        "home",
        shows=shows,
        **TEMPLATE_AUTH_KWARGS,
    )


@route("/delete", method="POST")
def delete():
    access_token = _get_access_token()
    item_type = request.query.item_type
    ids = request.forms.dict.get(item_type)

    if item_type == "playlists":
        for id in ids:
            requests.delete(
                f"{BASE_URL}/playlists/{id}/followers",
                headers={"Authorization": f"Bearer {access_token}"},
            )
    else:
        if len(ids) > 50:
            for i in range(0, len(ids), 50):
                requests.delete(
                    f"{BASE_URL}/me/{item_type}?ids={','.join(ids[i:i+50])}",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
        else:
            requests.delete(
                f"{BASE_URL}/me/{item_type}?ids={','.join(ids)}",
                headers={"Authorization": f"Bearer {access_token}"},
            )

    redirect(f"/{request.query.redirect_to}")


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloader=True)
