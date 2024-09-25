<!DOCTYPE html>
<html>

<head>
  <title>Spotify Cleaner</title>
  <link rel="stylesheet" href="https://cdn.rawgit.com/Chalarangelo/mini.css/v3.0.1/dist/mini-default.min.css">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>
  <header>
    <a href="/" class="button">Spotify Cleaner</a>
    <a href="https://accounts.spotify.com/authorize?client_id={{CLIENT_ID}}&response_type=code&redirect_uri={{REDIRECT_URI}}&scope={{SCOPE}}"
      class="button">
      Login with Spotify
    </a>
  </header>

  <div class="container">
    <div class="row">
      <div class="col-sm-4">
        <p>
          This is a simple tool to help you clean up your Spotify account. You can use it to get a list of your liked
          songs,
          saved albums, playlists, and podcasts. You can then use this information to clean up your account by removing
          songs, albums, playlists, and podcasts that you no longer want.
        </p>
        <p>
          To get started, click the "Login with Spotify" button above. You will be redirected to Spotify to authorize
          the app. Once you authorize the app, you will be redirected back here and you can start cleaning up your
          account.
        </p>
        <br />
        <nav>
          <a href='/get-liked-songs'>
            Get Liked Songs
          </a>
          <a href='/get-saved-albums'>
            Get Saved Albums
          </a>
          <a href='/get-playlists'>Get Playlists</a>
          <a href='/get-podcasts'>Get Podcasts</a>
        </nav>
      </div>
      <div class="col-sm-8">
        {{!base}}
      </div>
    </div>
</body>

</html>