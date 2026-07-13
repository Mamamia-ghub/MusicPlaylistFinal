import os
from urllib.parse import urlencode
from services.base_service import BaseNetworkService


class LastFMService(BaseNetworkService):
    BASE_URL = "https://ws.audioscrobbler.com/2.0/"

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("LASTFM_API_KEY")

        if not self.api_key:
            raise ValueError("LASTFM_API_KEY environment variable is missing")

    def _build_request(self, method, **params):
        """
        Builds a Last.fm API request URL.
        """
        query_params = {
            "method": method,
            "api_key": self.api_key,
            "format": "json",
            **params
        }

        return f"{self.BASE_URL}?{urlencode(query_params)}"

    def search(self, query, search_type="track"):
        """
        Search artists, albums, or tracks.
        """
        search_type = search_type.lower().strip()

        if search_type.endswith("s"):
            search_type = search_type[:-1]

        valid_types = {
            "artist",
            "album",
            "track"
        }

        if search_type not in valid_types:
            raise ValueError("Search type must be artist, album, or track")

        url = self._build_request(
            f"{search_type}.search",
            **{search_type: query.strip()}
        )

        return self._safe_get(url)

    def get_artist_info(self, artist_name):
        """
        Get artist biography information.
        """
        url = self._build_request(
            "artist.getInfo",
            artist=artist_name.strip()
        )

        return self._safe_get(url)

    def get_artist_tracks(self, artist_name):
        """
        Get an artist's top tracks.
        """
        url = self._build_request(
            "artist.getTopTracks",
            artist=artist_name.strip()
        )

        return self._safe_get(url)

    def get_similar_artists(self, artist_name):
        """
        Get similar artists.
        """
        url = self._build_request(
            "artist.getSimilar",
            artist=artist_name.strip()
        )

        return self._safe_get(url)

    def get_tag_tracks(self, tag_name):
        """
        Get popular tracks by genre/tag.
        """
        url = self._build_request(
            "tag.getTopTracks",
            tag=tag_name.strip()
        )

        return self._safe_get(url)

