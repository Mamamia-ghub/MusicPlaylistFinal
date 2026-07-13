MusicExplorers Portal Engine

web platform built on Flask to catalog listening history logs, manage playlists, view artist analytics, and discover music using Last.fm external metadata REST API.

WEB URL: https://mamamiamaria1.pythonanywhere.com/

---

Highlights

**Application Structure:** Application is fully set up in `create_app()`

**Blueprint Organization:** The project is divided into separate modules (`auth_bp`, `main_bp`, `api_bp`)

**Database System:** Uses Flask-SQLAlchemy with 6 related SQLite tables connected through foreign keys and automatic deletion rules.

**User Authentication:** Uses Werkzeug password hashing, Flask sessions, and a custom `@login_required` decorator to protect user-only pages (can't access My Playlists and Stats & Trending if not logged in)

**REST API:** Provides 6 JSON API endpoints under `/api/` for sending and receiving application data.

**User Interaction:** Uses HTMX(no javascript) for deleting playlists, and CSS `:target` selectors for review popups.

**Experience:** Includes search features, formatted dates, and navigation between pages.

---

Features Implemented

1. **Last.fm Music Search:** Allows users to search for artists, albums, and tracks using live Last.fm data.

2. **Playlist Management System:** Supports creating and deleting playlists with database management features.

3. **Track Ordering System:** Allows users to control the order of tracks inside playlists.

4. **Track Review System:** Provides a review popup where users can rate tracks from 1-5 stars and write comments up to 280 characters.

5. **Listening History Tracking:** Saves user listening activity.

6. **Artist Information Pages:** Displays artist biographies and top tracks using Last.fm data.

7. **Similar Artist Recommendations:** Suggests related artists using Last.fm recommendations.

8. **Monthly Statistics:** Shows user listening statistics, including top artists and categories for each month.

9. **Public Playlist Sharing:** Creates shareable public playlist pages with read-only access.

10. **Genre and Tag Explorer:** Allows users to discover tracks by exploring music categories and tags.

11. **Trending Music System:** Displays the most listened-to tracks based on user activity from the last 7 days.

---
## **Guide and explanation of structure**
<img width="1000" height="1000" alt="Skeleton1" src="https://github.com/user-attachments/assets/18414618-cb83-4b0e-bc5e-9c62dd7001f1" />
<img width="1000" height="1000" alt="Skeleton2" src="https://github.com/user-attachments/assets/07b06c2b-0124-4672-84ec-4d6294b3f75b" />

---
## **api.py Code breakdown and explanation**
<img width="1000" height="1000" alt="api py1" src="https://github.com/user-attachments/assets/66eec792-7df3-48d2-b9fc-9f17fe5a0c36" />
<img width="1000" height="1000" alt="api py2" src="https://github.com/user-attachments/assets/33dc352b-cfa7-4e09-a134-2b56381291be" />
<img width="1000" height="1000" alt="api py3" src="https://github.com/user-attachments/assets/7fb167d2-2667-4be2-bc6f-74ebc1c8739e" />

---
## **auth.py Code breakdown and explanation**
<img width="1000" height="1000" alt="auth py1" src="https://github.com/user-attachments/assets/5af8ae71-b18d-471e-8d1f-56053c1b40a2" />
<img width="1000" height="1000" alt="auth py2" src="https://github.com/user-attachments/assets/39af1e4f-f50e-4502-bb76-ad1462e608c9" />
<img width="1000" height="1000" alt="auth py3" src="https://github.com/user-attachments/assets/815abc8f-a0a6-4a28-8c55-87af7fdbdcac" />

---
## **main.py Code breakdown and explanation**
<img width="1000" height="1000" alt="main py1" src="https://github.com/user-attachments/assets/077a6319-337b-47cb-a650-8e99c59b320f" />
<img width="1000" height="1000" alt="main py2" src="https://github.com/user-attachments/assets/74fc2e5e-1366-4b4b-b9bf-49914c22a089" />
<img width="1000" height="1000" alt="main py3" src="https://github.com/user-attachments/assets/6eae0262-0c98-4cfa-b380-678a02f5752a" />
<img width="1000" height="1000" alt="main py4" src="https://github.com/user-attachments/assets/a3f90bd8-b2bc-4669-af78-9f704377ffdf" />
<img width="1000" height="1000" alt="main py4" src="https://github.com/user-attachments/assets/d767929c-6343-4dd2-8cef-f1b88f7c6870" />
<img width="1000" height="1000" alt="main py5" src="https://github.com/user-attachments/assets/ac2ed769-a1e7-4368-bc0a-bf93f57a8e65" />
<img width="1000" height="1000" alt="main py6" src="https://github.com/user-attachments/assets/7a8d44cb-1ddb-4866-bd5a-db0ebb5c1dc5" />



















<!-- PROJECT THAT I'VE DONE -->
<!-- Project 24 — Music Discovery and Playlist Platform
**Field:** Music / Entertainment

### Mandatory Features
1. Search Artist / Album / Track using Last.fm API
2. Playlist CRUD: title, description, cover URL, public/private
3. Add, remove, and reorder Tracks in a Playlist using an order field
4. Track Micro-Review: rating 1-5 and comment, maximum 280 characters
5. Listening History log: track plus timestamp
6. Artist detail: bio plus top tracks using Last.fm `artist.getInfo` and `artist.getTopTracks`
7. Similar Artists recommendation using Last.fm `artist.getSimilar`
8. Monthly stats: top 5 artists and top 3 genres this month
9. Playlist sharing: public URL with read-only view
10. Genre / Tag explorer using Last.fm `tag.getTopTracks`
11. Global trending: most listened tracks this week based on user logs

### REST API Endpoints
```http
GET    /api/search?q=                         — Last.fm proxy (artist/track)
GET    /api/playlists                         — user playlists
POST   /api/playlists                         — create playlist
POST   /api/playlists/<id>/tracks             — add track
DELETE /api/playlists/<id>/tracks/<track_id>  — remove track
GET    /api/stats/monthly                     — user monthly stats
```

### Database Models
```text
User:           id, username, email, password_hash, bio
Playlist:       id, user_id, title, description, cover_url, is_public
PlaylistTrack:  id, playlist_id, track_mbid, track_name, artist_name, order, added_at
Review:         id, user_id, track_mbid, track_name, artist_name, rating, content, created_at
ListeningLog:   id, user_id, track_mbid, track_name, artist_name, listened_at
FavoriteArtist: id, user_id, artist_name, artist_mbid, added_at
```

### External API
**Last.fm API** — `https://ws.audioscrobbler.com/2.0/?method=artist.search&artist={name}&api_key=KEY&format=json`
- Free API key: create an account on the Last.fm API website. -->
