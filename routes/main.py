from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from datetime import datetime, timedelta
from sqlalchemy import func

from models import db, Playlist, PlaylistTrack, Review, ListeningLog, FavoriteArtist
from services.lastfm_service import LastFMService
from .auth import login_required
from datetime import timezone

main_bp = Blueprint('main', __name__)
lastfm = LastFMService()

@main_bp.route('/')
def index():
    """Global trending dashboard view (Feature 11)."""
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

    trending = db.session.query(
        ListeningLog.track_name, ListeningLog.artist_name, ListeningLog.track_mbid, func.count(ListeningLog.id).label('play_count')
    ).filter(ListeningLog.listened_at >= one_week_ago)\
     .group_by(ListeningLog.track_name, ListeningLog.artist_name, ListeningLog.track_mbid)\
     .order_by(func.count(ListeningLog.id).desc())\
     .limit(10).all()
     
    return render_template('index.html', trending=trending)

@main_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """Search Artist / Album / Track using Last.fm API (Feature 1 & UX Filter/Search)."""
    results = None
    query = request.args.get('q', '')
    raw_type = request.args.get('type', 'track')
    
    search_type = raw_type.lower().strip()
    if search_type.endswith('s'):
        search_type = search_type[:-1]
    
    if query:
        api_data = lastfm.search(query, search_type)
        if search_type == 'track':
            results = api_data.get('results', {}).get('trackmatches', {}).get('track', [])
        elif search_type == 'artist':
            results = api_data.get('results', {}).get('artistmatches', {}).get('artist', [])
        elif search_type == 'album':
            results = api_data.get('results', {}).get('albummatches', {}).get('album', [])

    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    trending = db.session.query(
        ListeningLog.track_name, ListeningLog.artist_name, ListeningLog.track_mbid, func.count(ListeningLog.id).label('play_count')
    ).filter(ListeningLog.listened_at >= one_week_ago)\
     .group_by(ListeningLog.track_name, ListeningLog.artist_name, ListeningLog.track_mbid)\
     .order_by(func.count(ListeningLog.id).desc())\
     .limit(10).all()

    return render_template('index.html', results=results, query=query, search_type=search_type, trending=trending)

@main_bp.route('/playlists')
@login_required
def playlists_dashboard():
    """Playlist Read Dashboard with pagination structure (UX Pagination)."""
    page = request.args.get('page', 1, type=int)
    pagination = Playlist.query.filter_by(user_id=session['user_id'])\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('playlists.html', pagination=pagination)

@main_bp.route('/playlists/create', methods=['POST'])
@login_required
def create_playlist():
    """Playlist CRUD: Create pipeline operation (Feature 2)."""
    title = request.form.get('title')
    description = request.form.get('description', '')
    cover_url = request.form.get('cover_url', '')
    is_public = 'is_public' in request.form

    if not title:
        flash("Playlist structural designation title is required.", "danger")
        return redirect(url_for('main.playlists_dashboard'))

    playlist = Playlist(
        user_id=session['user_id'], title=title, description=description,
        cover_url=cover_url, is_public=is_public
    )
    db.session.add(playlist)
    db.session.commit()
    flash(f"Playlist matrix '{title}' spawned successfully.", "success")
    return redirect(url_for('main.playlists_dashboard'))

@main_bp.route('/log-play', methods=['POST'])
@login_required
def log_listening_history():
    """Listening History log generation framework processing (Feature 5)."""
    track_name = request.form.get('track_name')
    artist_name = request.form.get('artist_name')
    track_mbid = request.form.get('track_mbid', '')

    log = ListeningLog(user_id=session['user_id'], track_name=track_name, artist_name=artist_name, track_mbid=track_mbid)
    db.session.add(log)
    db.session.commit()
    flash(f"Logged playback event stream: {track_name} by {artist_name}.", "info")
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/review/submit', methods=['POST'])
@login_required
def submit_review():
    """Track Micro-Review framework validation setup constraints (Feature 4)."""
    track_name = request.form.get('track_name')
    artist_name = request.form.get('artist_name')
    track_mbid = request.form.get('track_mbid', '')
    try:
        rating = int(request.form.get('rating', 5))
    except ValueError:
        rating = 5
    content = request.form.get('content', '')

    if len(content) > 280:
        flash("Micro-review exceeds structural limit constraint of 280 characters.", "danger")
        return redirect(request.referrer or url_for('main.index'))

    review = Review(
        user_id=session['user_id'], track_name=track_name, artist_name=artist_name,
        track_mbid=track_mbid, rating=rating, content=content
    )
    db.session.add(review)
    db.session.commit()
    flash("Micro-review entry configuration archived successfully.", "success")
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/artist/<string:artist_name>')
def artist_profile(artist_name):
    """Artist detail bio, top tracks, and recommendations aggregation (Feature 6 & 7)."""
    bio_data = lastfm.get_artist_info(artist_name).get('artist', {})
    top_tracks = lastfm.get_artist_tracks(artist_name).get('toptracks', {}).get('track', [])[:5]
    similar = lastfm.get_similar_artists(artist_name).get('similarartists', {}).get('artist', [])[:5]
    return render_template('artist.html', bio=bio_data, top_tracks=top_tracks, similar=similar)

@main_bp.route('/genre/<string:tag_name>')
def genre_explorer(tag_name):
    """Genre / Tag ecosystem discovery explorer (Feature 10)."""
    tag_tracks = lastfm.get_tag_tracks(tag_name).get('tracks', {}).get('track', [])[:15]
    
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    trending = db.session.query(
        ListeningLog.track_name, ListeningLog.artist_name, ListeningLog.track_mbid, func.count(ListeningLog.id).label('play_count')
    ).filter(ListeningLog.listened_at >= one_week_ago)\
     .group_by(ListeningLog.track_name, ListeningLog.artist_name, ListeningLog.track_mbid)\
     .order_by(func.count(ListeningLog.id).desc())\
     .limit(10).all()

    return render_template('index.html', results=tag_tracks, search_type='track', query=f"Genre: {tag_name}", trending=trending)

@main_bp.route('/stats')
@login_required
def stats_dashboard():
    """Monthly system analytic processing logic matrix metrics (Feature 8)."""
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    query_artists = db.session.query(
        ListeningLog.artist_name, func.count(ListeningLog.id).label('play_count')
    ).filter(
        func.strftime('%m', ListeningLog.listened_at) == f"{current_month:02d}",
        func.strftime('%Y', ListeningLog.listened_at) == str(current_year),
        ListeningLog.user_id == session['user_id']
    ).group_by(ListeningLog.artist_name)\
     .order_by(func.count(ListeningLog.id).desc())\
     .limit(5).all()

    top_artists = []
    for artist in query_artists:
        calculated_width = min(artist.play_count * 10, 100)
        top_artists.append({
            'artist_name': artist.artist_name,
            'play_count': artist.play_count,
            'width': calculated_width
        })

    mock_genres = [("Alternative Rock", 14), ("Synthwave", 9), ("Electronic", 5)]
    return render_template('stats.html', top_artists=top_artists, top_genres=mock_genres)

@main_bp.route('/playlists/delete/<int:playlist_id>', methods=['DELETE'])
@login_required
def delete_playlist_matrix(playlist_id):
    playlist = Playlist.query.filter_by(id=playlist_id, user_id=session['user_id']).first_or_404()
    
    db.session.delete(playlist)
    db.session.commit()
    
    return "", 200



