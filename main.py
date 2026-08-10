import requests
from bottle import abort, redirect, request, response, route, run, template

from config import (
    BASE_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    LIBRARY_ITEMS_LIMIT,
    REDIRECT_URI,
    RESPONSE_ITEMS_LIMIT,
    TEMPLATE_AUTH_KWARGS,
    URI_TYPE,
)


def _abort_with_api_error(res):
    try:
        message = res.json()["error"]["message"]
    except (ValueError, KeyError):
        message = res.text or res.reason
    abort(res.status_code, message)


def _get_access_token():
    access_token = request.get_cookie("access_token")
    if access_token is None:
        abort(401, "Error: access_token not provided")

    return access_token


def _render_home(**kwargs):
    deleted = request.query.deleted
    if deleted:
        kwargs["deleted_count"] = int(deleted)
    return template("home", **kwargs, **TEMPLATE_AUTH_KWARGS)


@route("/")
def main():
    return _render_home()


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
        try:
            message = res.json()["error_description"]
        except (ValueError, KeyError):
            message = res.text or res.reason
        abort(res.status_code, message)

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
        _abort_with_api_error(res)

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

    return _render_home(tracks=tracks)


@route("/get-saved-albums")
def get_saved_albums():
    access_token = _get_access_token()
    albums = _get_items(
        access_token,
        "albums",
        0,
    )

    return _render_home(albums=albums)


@route("/get-playlists")
def get_playlists():
    access_token = _get_access_token()
    playlists = _get_items(
        access_token,
        "playlists",
        0,
    )

    return _render_home(playlists=playlists)


@route("/get-podcasts")
def get_podcasts():
    access_token = _get_access_token()
    shows = _get_items(
        access_token,
        "shows",
        0,
    )

    return _render_home(shows=shows)


@route("/get-episodes")
def get_episodes():
    access_token = _get_access_token()
    episodes = _get_items(
        access_token,
        "episodes",
        0,
    )

    return _render_home(episodes=episodes)


@route("/delete", method="POST")
def delete():
    access_token = _get_access_token()
    item_type = request.query.item_type
    ids = [id for id in request.forms.dict.get(item_type, []) if id]

    if not ids:
        abort(400, "Error: no items selected")

    uri_type = URI_TYPE[item_type]
    for i in range(0, len(ids), LIBRARY_ITEMS_LIMIT):
        uris = [f"spotify:{uri_type}:{id}" for id in ids[i : i + LIBRARY_ITEMS_LIMIT]]
        res = requests.delete(
            f"{BASE_URL}/me/library",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"uris": ",".join(uris)},
        )
        if res.status_code != 200:
            _abort_with_api_error(res)

    redirect(f"/{request.query.redirect_to}?deleted={len(ids)}")


if __name__ == "__main__":
    run(host="127.0.0.1", port=8080, debug=True, reloader=True)
