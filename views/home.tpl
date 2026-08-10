% rebase('base.tpl')
<div class="row">
  <div class="col-sm-12">

    % if defined('tracks'):
    <form action="/delete?redirect_to=get-liked-songs&item_type=tracks" method="POST">
      <legend>Liked Songs ({{len(tracks)}})</legend>
      % include('form_header.tpl')
      <div>
        % for track in tracks:
        % if track.get('track') and track['track'].get('id'):
        <fieldset>
          <input type="checkbox" id="{{track['track']['id']}}" name="tracks" value="{{track['track']['id']}}" />
          <label for="{{track['track']['id']}}">{{track["track"]["name"]}} -
            {{track["track"]["artists"][0]["name"]}}</label>
        </fieldset>
        % end
        % end
      </div>
    </form>
    % end

    % if defined('albums'):
    <form action="/delete?redirect_to=get-saved-albums&item_type=albums" method="POST">
      <legend>Saved Albums ({{len(albums)}})</legend>
      % include('form_header.tpl')
      <div>
        % for album in albums:
        % if album.get('album') and album['album'].get('id'):
        <fieldset>
          <input type="checkbox" id="{{album['album']['id']}}" name="albums" value="{{album['album']['id']}}" />
          <label for="{{album['album']['id']}}">{{album["album"]["name"]}} -
            {{album["album"]["artists"][0]["name"]}}</label>
        </fieldset>
        % end
        % end
      </div>
    </form>
    % end

    % if defined('playlists'):
    <form action="/delete?redirect_to=get-playlists&item_type=playlists" method="POST">
      <legend>Playlists ({{len(playlists)}})</legend>
      % include('form_header.tpl')
      <div>
        % for playlist in playlists:
        % if playlist.get('id'):
        <fieldset>
          <input type="checkbox" id="{{playlist['id']}}" name="playlists" value="{{playlist['id']}}" />
          <label for="{{playlist['id']}}">{{playlist["name"]}}</label>
        </fieldset>
        % end
        % end
      </div>
    </form>
    % end

    % if defined('shows'):
    <form action="/delete?redirect_to=get-podcasts&item_type=shows" method="POST">
      <legend>Podcasts ({{len(shows)}})</legend>
      % include('form_header.tpl')
      <div>
        % for show in shows:
        % if show.get('show') and show['show'].get('id'):
        <fieldset>
          <input type="checkbox" id="{{show['show']['id']}}" name="shows" value="{{show['show']['id']}}" />
          <label for="{{show['show']['id']}}">{{show["show"]["name"]}}</label>
        </fieldset>
        % end
        % end
      </div>
    </form>
    % end

    % if defined('episodes'):
    <form action="/delete?redirect_to=get-episodes&item_type=episodes" method="POST">
      % selectable_episodes = [e for e in episodes if e.get('episode') and e['episode'].get('id')]
      <legend>Your Episodes ({{len(selectable_episodes)}} removable of {{len(episodes)}})</legend>
      % include('form_header.tpl')
      <p><small>Spotify limits deletions to 40 at a time. "Select All" + "Delete Selected" runs all of them in one click,
          but for very large libraries you may need to click "Delete Selected" more than once if Spotify throttles the
          requests.</small></p>
      <div>
        % for episode in selectable_episodes:
        <fieldset>
          <input type="checkbox" id="{{episode['episode']['id']}}" name="episodes" value="{{episode['episode']['id']}}" />
          <label for="{{episode['episode']['id']}}">{{episode["episode"]["name"]}} -
            {{episode["episode"]["show"]["name"]}}</label>
        </fieldset>
        % end
      </div>
    </form>
    % end

  </div>
</div>

<script type="text/javascript">
  const toggleSelectAllCheckboxes = (event) => {
    const checkboxes = document.querySelectorAll('input[type=checkbox]');
    checkboxes.forEach((cb) => { cb.checked = event.target.checked; });
  }
</script>
