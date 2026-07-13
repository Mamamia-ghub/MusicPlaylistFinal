from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, default="")
    
    playlists = db.relationship('Playlist', backref='owner', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='author', lazy=True)
    logs = db.relationship('ListeningLog', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    cover_url = db.Column(db.String(255), default="")
    is_public = db.Column(db.Boolean, default=True)
    
    tracks = db.relationship('PlaylistTrack', backref='playlist', lazy=True, order_by="PlaylistTrack.order", cascade="all, delete-orphan")

class PlaylistTrack(db.Model):
    __tablename__ = 'playlist_tracks'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    track_mbid = db.Column(db.String(100), default="")
    track_name = db.Column(db.String(255), nullable=False)
    artist_name = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, default=0, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    track_mbid = db.Column(db.String(100), default="")
    track_name = db.Column(db.String(255), nullable=False)
    artist_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False) 
    content = db.Column(db.String(280), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ListeningLog(db.Model):
    __tablename__ = 'listening_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    track_mbid = db.Column(db.String(100), default="")
    track_name = db.Column(db.String(255), nullable=False)
    artist_name = db.Column(db.String(255), nullable=False)
    listened_at = db.Column(db.DateTime, default=datetime.utcnow)

class FavoriteArtist(db.Model):
    __tablename__ = 'favorite_artists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artist_name = db.Column(db.String(255), nullable=False)
    artist_mbid = db.Column(db.String(100), default="")
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

