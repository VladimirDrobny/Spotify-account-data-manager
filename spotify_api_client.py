import spotipy

scope = "user-modify-playback-state user-library-modify user-library-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-follow-modify user-follow-read user-read-private user-read-email"

class SpotifyApiClient:
    def __init__(self, _client_id, _client_secret, _redirect_uri, _FORCED_FOLLOW_USER_LIST):
        self.FORCED_FOLLOW_USER_LIST = _FORCED_FOLLOW_USER_LIST
        self.sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(
            scope=scope,
            client_id=_client_id,
            client_secret=_client_secret,
            redirect_uri=_redirect_uri,
            show_dialog=True,
            open_browser=True,
            cache_handler=spotipy.cache_handler.MemoryCacheHandler()
        ))

    def get_logged_in_status(self):
        try:
            self.sp.me()
            return True
        except:
            pass
        return False

    def get_username(self):
        return self.sp.me()["display_name"]

    def get_account_data(self):
        '''
        RETURN TEMPLATE:
        {
                "saved_tracks":[TRACK_IDS],
                "saved_albums":[ALBUM_IDS],
                "created_playlists":[{
                    "name":NAME,
                    "description":DESCRIPTION,
                    "id":PLAYLIST_ID,
                    "tracks":[TRACK_IDS]
                }],
                "saved_playlists":[PLAYLIST_IDS],
                "followed_artists":[ARTISTS_IDS],
                "followed_users":[USER_IDS]
        }
        '''

        return {
                "saved_tracks":self.get_saved_tracks(),
                "saved_albums":self.get_saved_albums(),
                "created_playlists":self.get_created_playlists(),
                "saved_playlists":self.get_saved_playlists(),
                "followed_artists":self.get_followed_artists(),
                "followed_users":self.get_followed_users()
        }
        return None

    def get_saved_tracks(self):
        ret = []
        data_saved_tracks = self._get_all_saved_tracks_unformatted()
        for track in data_saved_tracks:
            ret.append(track["track"]["id"])
        return ret

    def _get_all_saved_tracks_unformatted(self):
        results = self.sp.current_user_saved_tracks()
        tracks = results["items"]
        while results["next"]:
            results = self.sp.next(results)
            tracks.extend(results["items"])
        return tracks

    def get_saved_albums(self):
        ret = []
        data_saved_albums = self._get_all_saved_albums_unformatted()
        for album in data_saved_albums:
            ret.append(album["album"]["id"])
        return ret

    def _get_all_saved_albums_unformatted(self):
        results = self.sp.current_user_saved_albums()
        albums = results["items"]
        while results["next"]:
            results = self.sp.next(results)
            albums.extend(results["items"])
        return albums

    def _get_all_playlists(self):
        results = self.sp.current_user_playlists()
        playlists = results["items"]
        while results["next"]:
            results = self.sp.next(results)
            playlists.extend(results["items"])
        return playlists

    def _get_tracks_from_playlist_unformatted(self, playlist_id):
        results = self.sp.playlist_items(playlist_id)
        tracks = results["items"]
        while results["next"]:
            results = self.sp.next(results)
            tracks.extend(results["items"])
        return tracks

    def _get_tracks_from_playlist(self, playlist_id):
        data_playlist_tracks = self._get_tracks_from_playlist_unformatted(playlist_id)
        ret = []
        for track in data_playlist_tracks:
            ret.append(track["track"]["id"])
        return ret

    def _get_created_playlist_data(self, playlist):
        return {
                "name":playlist["name"],
                "description":playlist["description"],
                "id":playlist["id"],
                "tracks":self._get_tracks_from_playlist(playlist["id"])
        }

    def _get_all_playlists_of_type_unformatted(self, original):
        data_playlists = self._get_all_playlists()
        self_id = self.sp.me()["id"]
        ret = []
        for playlist in data_playlists:
            if ((playlist["owner"]["id"] == self_id) == original):
                ret.append(playlist)
        return ret

    def get_created_playlists(self):
        ret = []
        data_playlists = self._get_all_playlists_of_type_unformatted(True)
        for playlist in data_playlists:
            ret.append(self._get_created_playlist_data(playlist))
        return ret

    def get_saved_playlists(self):
        ret = []
        data_playlists = self._get_all_playlists_of_type_unformatted(False)
        for playlist in data_playlists:
            ret.append(playlist["id"])
        return ret

    def get_followed_users(self):
        #Spotify API doesn't support this at the moment.
        #Returning hardcoded data instead.
        return self.FORCED_FOLLOW_USER_LIST 

    def _get_followed_artists_unformatted(self):
        results = self.sp.current_user_followed_artists()["artists"]
        artists = results["items"]
        while results["next"]:
            results = self.sp.next(results)["artists"]
            artists.extend(results["items"])
        return artists
        
    def get_followed_artists(self):
        ret = []
        data_followed_artists = self._get_followed_artists_unformatted()
        for artist in data_followed_artists:
            ret.append(artist["id"])
        return ret

    def add_account_data(self, new_data):
        current_user_id = self.sp.me()["id"]

        temp_ids = new_data["saved_tracks"]
        while(temp_ids):
            self.sp.current_user_saved_tracks_add(temp_ids[:50])
            temp_ids = temp_ids[50:]
        
        temp_ids = new_data["saved_albums"]
        while(temp_ids):
            self.sp.current_user_saved_albums_add(temp_ids[:20])
            temp_ids = temp_ids[20:]
        
        temp_ids = new_data["followed_artists"]
        while(temp_ids):
            self.sp.user_follow_artists(temp_ids[:50])
            temp_ids = temp_ids[50:]
        
        temp_ids = new_data["followed_users"]
        while(temp_ids):
            self.sp.user_follow_users(temp_ids[:50])
            temp_ids = temp_ids[50:]

        for playlist_id in new_data["saved_playlists"]:
            self.sp.current_user_follow_playlist(playlist_id)

        for playlist in new_data["created_playlists"]:
            new_playlist = self.sp.user_playlist_create(current_user_id, playlist["name"], public=False, collaborative=False, description=playlist["description"])
            if (new_playlist):
                temp_ids = playlist["tracks"]
                while(temp_ids):
                    self.sp.playlist_add_items(new_playlist["id"], temp_ids[:100])
                    temp_ids = temp_ids[100:]
            else:
                print("ERROR OCCURED WHEN CREATING PLAYLIST!")

    def wipe_account(self):
        account_data = self.get_account_data()
        
        current_user_id = self.sp.me()["id"]

        temp_ids = account_data["saved_tracks"]
        while(temp_ids):
            self.sp.current_user_saved_tracks_delete(temp_ids[:50])
            temp_ids = temp_ids[50:]
        
        temp_ids = account_data["saved_albums"]
        while(temp_ids):
            self.sp.current_user_saved_albums_delete(temp_ids[:20])
            temp_ids = temp_ids[20:]
        
        temp_ids = account_data["followed_artists"]
        while(temp_ids):
            self.sp.user_unfollow_artists(temp_ids[:50])
            temp_ids = temp_ids[50:]
        
        temp_ids = account_data["followed_users"]
        while(temp_ids):
            self.sp.user_unfollow_users(temp_ids[:50])
            temp_ids = temp_ids[50:]

        for playlist_id in account_data["saved_playlists"]:
            self.sp.current_user_unfollow_playlist(playlist_id)

        for playlist in account_data["created_playlists"]:
            self.sp.current_user_unfollow_playlist(playlist["id"]) 
