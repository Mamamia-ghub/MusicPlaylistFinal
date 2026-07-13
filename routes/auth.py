from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from models import User, db

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Custom security access verification decorator."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please authenticate secure identity credentials to access this matrix.", "danger")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash("Username or Email configuration collisions located.", "danger")
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Account configuration finalized. Please proceed to sign in.", "success")
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f"Session established. Welcome back, user {user.username}!", "success")
            return redirect(url_for('main.playlists_dashboard'))
            
        flash("Invalid identification credentials assigned.", "danger")
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Session context workspace closed safely.", "info")
    return redirect(url_for('auth.login'))
