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
