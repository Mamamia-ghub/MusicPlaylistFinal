from flask import Blueprint, jsonify, request, session
from datetime import datetime
from sqlalchemy import func

from models import db, Playlist, PlaylistTrack, ListeningLog
from services.lastfm_service import LastFMService

api_bp = Blueprint('api', __name__, url_prefix='/api')
lastfm = LastFMService()


@api_bp.route("/search", methods=["GET"])
def api_search_proxy():
    """
    GET /api/search?q=&type=track
    Proxy search request to Last.fm.
    """
    query = request.args.get("q", "").strip()
    search_type = request.args.get("type", "track")

    if not query:
        return jsonify({"error": "Missing search query."}), 400

    data = lastfm.search(query, search_type)
    return jsonify(data), 200


@api_bp.route("/playlists", methods=["GET"])
def api_get_playlists():
    """
    GET /api/playlists
    Return playlists for the logged-in user.
    """
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    playlists = Playlist.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": playlist.id,
            "title": playlist.title,
            "description": playlist.description,
            "is_public": playlist.is_public,
        }
        for playlist in playlists
    ]), 200


@api_bp.route("/playlists", methods=["POST"])
def api_create_playlist():
    """
    POST /api/playlists
    Create a new playlist.
    """
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}

    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Playlist title is required."}), 400

    playlist = Playlist(
        user_id=user_id,
        title=title,
        description=data.get("description", ""),
        cover_url=data.get("cover_url", ""),
        is_public=data.get("is_public", True),
    )

    db.session.add(playlist)
    db.session.commit()

    return jsonify({
        "success": True,
        "created_id": playlist.id
    }), 201


@api_bp.route("/playlists/<int:id>/tracks", methods=["POST"])
def api_add_track(id):
    """
    POST /api/playlists/<id>/tracks
    Add a track to a playlist.
    """
    playlist = Playlist.query.get_or_404(id)

    data = request.get_json() or {}

    track_name = data.get("track_name", "").strip()
    artist_name = data.get("artist_name", "").strip()

    if not track_name or not artist_name:
        return jsonify({
            "error": "track_name and artist_name are required."
        }), 400

    highest_order = (
        db.session.query(func.max(PlaylistTrack.order))
        .filter(PlaylistTrack.playlist_id == playlist.id)
        .scalar()
        or 0
    )

    new_track = PlaylistTrack(
        playlist_id=playlist.id,
        track_name=track_name,
        artist_name=artist_name,
        track_mbid=data.get("track_mbid", ""),
        order=highest_order + 1,
    )

    db.session.add(new_track)
    db.session.commit()

    return jsonify({
        "success": True,
        "added_track_id": new_track.id
    }), 201


@api_bp.route("/playlists/<int:id>/tracks/<int:track_id>", methods=["DELETE"])
def api_remove_track(id, track_id):
    """
    DELETE /api/playlists/<id>/tracks/<track_id>
    Remove a track from a playlist.
    """
    track = PlaylistTrack.query.filter_by(
        id=track_id,
        playlist_id=id
    ).first()

    if not track:
        return jsonify({"error": "Track not found."}), 404

    db.session.delete(track)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Track removed successfully."
    }), 200


@api_bp.route("/stats/monthly", methods=["GET"])
def api_monthly_stats():
    """
    GET /api/stats/monthly
    Simple placeholder endpoint.
    """
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "current_reporting_status": "Active"
    }), 200
